# Lớp Student (Sinh viên) - Kế thừa từ UserRecord
# Thuộc tính riêng: studentID, programID, status, semesterGPA (tính toán), cumulativeGPA (tính toán)
# Phương thức: viewTrainingProgram, viewGrades, viewGPA, calculateSemesterGPA, calculateCumulativeGPA

from models.user_record import UserRecord
from utils.file_handler import (read_records, find_record, find_all_records,
                                 update_record, append_line, delete_record)
from utils.validators import validate_email, validate_phone


class Student(UserRecord):
    # Tên file lưu trữ dữ liệu sinh viên
    FILE = "students.txt"

    def __init__(self, studentID, cccd, fullName, dob, email, gender,
                 phoneNumber, facultyCode, programID="", status="Active"):
        # Gọi hàm khởi tạo của lớp cha UserRecord
        super().__init__(cccd, fullName, dob, email, gender, phoneNumber)
        self._studentID = studentID       # Mã số sinh viên
        self._facultyCode = facultyCode   # Mã khoa (FK tới Faculty)
        self._programID = programID       # Mã chương trình đào tạo
        self._status = status             # Trạng thái (Active/Inactive)
        self._semesterGPA = 0.0           # GPA học kỳ (thuộc tính tính toán)
        self._cumulativeGPA = 0.0         # GPA tích lũy (thuộc tính tính toán)

    # Thuộc tính

    @property
    def studentID(self):
        return self._studentID

    @property
    def facultyCode(self):
        return self._facultyCode

    @property
    def programID(self):
        return self._programID

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def semesterGPA(self):
        # Thuộc tính tính toán - GPA học kỳ
        return self._semesterGPA

    @property
    def cumulativeGPA(self):
        # Thuộc tính tính toán - GPA tích lũy
        return self._cumulativeGPA

    # Chuyển đổi dữ liệu

    def to_record(self):
        # Chuyển đối tượng thành danh sách trường để lưu file
        return [self._studentID, self._cccd, self._fullName, self._dob,
                self._email, self._gender, self._phoneNumber,
                self._facultyCode, self._programID, self._status]

    @staticmethod
    def from_record(record):
        # Tạo đối tượng Student từ bản ghi file
        if len(record) >= 10:
            return Student(*record[:10])
        return None

    # Phương thức theo Class Diagram

    def updatePersonalInfo(self, **kwargs):
        # UC7: Sinh viên chỉ được sửa Email và Số điện thoại
        email = kwargs.get("email", self._email)
        phone = kwargs.get("phoneNumber", self._phoneNumber)
        if not validate_email(email):
            return False, "Invalid email format."
        if not validate_phone(phone):
            return False, "Invalid phone number."
        self._email = email
        self._phoneNumber = phone
        if update_record(self.FILE, 0, self._studentID, self.to_record()):
            return True, "Profile updated successfully."
        return False, "Failed to update profile."

    def viewTrainingProgram(self):
        # UC15: Xem chương trình đào tạo với trạng thái Hoàn thành/Chưa hoàn thành
        from models.training_program import TrainingProgram
        program = TrainingProgram.find_by_id(self._programID)
        return program

    def viewGrades(self):
        # Xem bảng điểm học vụ: chỉ trả về các bản ghi đã duyệt (Finalized)
        from models.grade import Grade
        return [g for g in Grade.find_by_student(self._studentID) if g.status == "Finalized"]

    def viewGPA(self):
        # Xem giá trị GPA hiện tại
        return self._semesterGPA, self._cumulativeGPA

    def calculateSemesterGPA(self, semesterCode=""):
        # Tính GPA cho một học kỳ cụ thể dựa trên điểm đã duyệt (Finalized)
        from models.grade import Grade
        grades = Grade.find_by_student(self._studentID)

        if semesterCode:
            # Lọc điểm theo học kỳ
            from models.class_section import ClassSection
            semester_grades = []
            for g in grades:
                if g.status == "Finalized":
                    cs = ClassSection.find_by_code(g.classCode)
                    if cs and cs.semesterCode == semesterCode:
                        semester_grades.append(g)
            grades = semester_grades
        else:
            # Nếu không chỉ định học kỳ, lấy tất cả điểm đã duyệt
            grades = [g for g in grades if g.status == "Finalized"]

        if not grades:
            return 0.0

        # Tính GPA theo công thức: tổng(điểm × tín chỉ) / tổng(tín chỉ)
        from models.class_section import ClassSection
        from models.course import Course
        total_points = 0.0
        total_credits = 0
        for g in grades:
            cs = ClassSection.find_by_code(g.classCode)
            if cs:
                course = Course.find_by_code(cs.courseCode)
                if course:
                    credits = course.credits
                    total_points += g.finalSummaryGrade * credits
                    total_credits += credits
        self._semesterGPA = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
        return self._semesterGPA

    def calculateCumulativeGPA(self):
        # Tính GPA tích lũy qua tất cả các điểm đã duyệt
        from models.grade import Grade
        from models.class_section import ClassSection
        from models.course import Course

        grades = [g for g in Grade.find_by_student(self._studentID) if g.status == "Finalized"]
        if not grades:
            return 0.0

        total_points = 0.0
        total_credits = 0
        for g in grades:
            cs = ClassSection.find_by_code(g.classCode)
            if cs:
                course = Course.find_by_code(cs.courseCode)
                if course:
                    credits = course.credits
                    total_points += g.finalSummaryGrade * credits
                    total_credits += credits
        self._cumulativeGPA = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
        return self._cumulativeGPA

    # Các hàm CRUD hỗ trợ

    def save(self):
        # Lưu hoặc cập nhật bản ghi sinh viên
        if find_record(self.FILE, 0, self._studentID):
            return update_record(self.FILE, 0, self._studentID, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    def delete(self):
        # Xóa bản ghi sinh viên khỏi file
        return delete_record(self.FILE, 0, self._studentID)

    @staticmethod
    def find_by_id(student_id):
        # Tìm sinh viên theo mã số
        record = find_record(Student.FILE, 0, student_id)
        return Student.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả sinh viên
        return [Student.from_record(r) for r in read_records(Student.FILE)
                if Student.from_record(r) is not None]
