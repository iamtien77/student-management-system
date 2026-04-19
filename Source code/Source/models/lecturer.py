# Lớp Lecturer (Giảng viên) - Kế thừa từ UserRecord
# Thuộc tính riêng: employeeID
# Phương thức: takeAttendance, inputComponentGrades, inputFinalExamGrade, saveDraft

from models.user_record import UserRecord
from utils.file_handler import (read_records, find_record, find_all_records,
                                 update_record, append_line, delete_record)
from utils.validators import validate_email, validate_phone


class Lecturer(UserRecord):
    # Tên file lưu trữ dữ liệu giảng viên
    FILE = "lecturers.txt"

    def __init__(self, employeeID, cccd, fullName, dob, email, gender,
                 phoneNumber, facultyCode):
        # Gọi hàm khởi tạo lớp cha
        super().__init__(cccd, fullName, dob, email, gender, phoneNumber)
        self._employeeID = employeeID     # Mã nhân viên
        self._facultyCode = facultyCode   # Mã khoa (FK tới Faculty)

    # Thuộc tính

    @property
    def employeeID(self):
        return self._employeeID

    @property
    def facultyCode(self):
        return self._facultyCode

    # Chuyển đổi dữ liệu

    def to_record(self):
        # Chuyển đối tượng thành danh sách trường để lưu file
        return [self._employeeID, self._cccd, self._fullName, self._dob,
                self._email, self._gender, self._phoneNumber, self._facultyCode]

    @staticmethod
    def from_record(record):
        # Tạo đối tượng Lecturer từ bản ghi file
        if len(record) >= 8:
            return Lecturer(*record[:8])
        return None

    # Phương thức theo Class Diagram

    def updatePersonalInfo(self, **kwargs):
        # UC7: Giảng viên chỉ được cập nhật Email và Số điện thoại (không đổi được Khoa)
        email = kwargs.get("email", self._email)
        phone = kwargs.get("phoneNumber", self._phoneNumber)
        if not validate_email(email):
            return False, "Invalid email format."
        if not validate_phone(phone):
            return False, "Invalid phone number."
        self._email = email
        self._phoneNumber = phone
        if update_record(self.FILE, 0, self._employeeID, self.to_record()):
            return True, "Profile updated successfully."
        return False, "Failed to update profile."

    def takeAttendance(self, classSection, studentID, status):
        # UC16: Điểm danh cho sinh viên trong một buổi học
        # Tạo bản ghi điểm danh mới với ngày hôm nay
        from models.attendance import Attendance
        from models.class_section import ClassSection
        import datetime

        # Chỉ cho điểm danh khi lớp tồn tại và đúng giảng viên phụ trách.
        persisted_class = ClassSection.find_by_code(classSection.classCode)
        if not persisted_class:
            return False, "Invalid class session."
        if persisted_class.lecturerID and persisted_class.lecturerID != self._employeeID:
            return False, "Invalid class session."

        session_date = datetime.date.today().strftime("%d/%m/%Y")
        att = Attendance(classSection.classCode, studentID, session_date, status)
        if att.markAttendance(status):
            return True, "Attendance recorded."
        return False, "Failed to record attendance."

    def inputComponentGrades(self, classCode, studentID, midterm, assignment, attendance_score):
        # UC17: Nhập điểm thành phần (giữa kỳ, bài tập, chuyên cần)
        # Nếu đã có điểm thì cập nhật, nếu chưa thì tạo mới
        from models.grade import Grade
        grade = Grade.find_by_student_class(studentID, classCode)
        # Không cho sửa nếu điểm đã duyệt
        if grade and grade.status == "Finalized":
            return False, "Grades have been finalized. Cannot edit."
        if grade:
            # Cập nhật điểm thành phần
            grade._midtermGrade = midterm
            grade._assignmentGrade = assignment
            grade._attendanceGrade = attendance_score
            grade.calculateFinalSummary()
            grade.assignLetterGrade()
            grade._status = "Draft"
            grade.save()
            return True, "Component grades updated."
        else:
            # Tạo bản ghi điểm mới
            grade = Grade(classCode, studentID, midterm, assignment,
                          attendance_score, 0.0, 0.0, "", "Draft")
            grade.calculateFinalSummary()
            grade.assignLetterGrade()
            grade.save()
            return True, "Component grades entered."

    def inputFinalExamGrade(self, classCode, studentID, finalExamGrade):
        # UC17: Nhập điểm thi cuối kỳ
        # Yêu cầu phải nhập điểm thành phần trước
        from models.grade import Grade
        grade = Grade.find_by_student_class(studentID, classCode)
        if not grade:
            return False, "No component grades found. Enter component grades first."
        if grade.status == "Finalized":
            return False, "Grades have been finalized. Cannot edit."
        grade._finalExamGrade = finalExamGrade
        grade.calculateFinalSummary()
        grade.assignLetterGrade()
        grade.save()
        return True, "Final exam grade entered."

    def saveDraft(self):
        # UC17: Xác nhận lưu tất cả điểm nháp hiện tại
        return True, "All grades saved as Draft."

    # Các hàm CRUD hỗ trợ

    def save(self):
        # Lưu hoặc cập nhật bản ghi giảng viên
        if find_record(self.FILE, 0, self._employeeID):
            return update_record(self.FILE, 0, self._employeeID, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    def delete(self):
        # Xóa bản ghi giảng viên
        return delete_record(self.FILE, 0, self._employeeID)

    @staticmethod
    def find_by_id(emp_id):
        # Tìm giảng viên theo mã nhân viên
        record = find_record(Lecturer.FILE, 0, emp_id)
        return Lecturer.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả giảng viên
        return [Lecturer.from_record(r) for r in read_records(Lecturer.FILE)
                if Lecturer.from_record(r) is not None]

    def get_assigned_classes(self):
        # Lấy danh sách các lớp học phần được phân công cho giảng viên này
        from models.class_section import ClassSection
        return ClassSection.find_by_lecturer(self._employeeID)
