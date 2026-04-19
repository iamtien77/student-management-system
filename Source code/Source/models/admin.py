# Lớp Admin (Quản trị viên) - Kế thừa từ UserRecord
# Thuộc tính riêng: adminID
# Phương thức: createAccount, manageStudent, manageLecturer, manageFaculty,
#              quanLyHocKy, quanLyMonHoc, quanLyLopHocPhan, phanCongGiangVien, chotDiem

from models.user_record import UserRecord
from utils.file_handler import find_record
from utils.validators import validate_not_empty, validate_credits


class Admin(UserRecord):
    # Quản trị viên có toàn quyền quản lý hệ thống

    def __init__(self, adminID="admin", cccd="", fullName="Administrator",
                 dob="", email="", gender="", phoneNumber=""):
        super().__init__(cccd, fullName, dob, email, gender, phoneNumber)
        self._adminID = adminID

    @property
    def adminID(self):
        return self._adminID

    def to_record(self):
        return [self._adminID, self._cccd, self._fullName, self._dob,
                self._email, self._gender, self._phoneNumber]

    @staticmethod
    def from_record(record):
        if len(record) >= 1:
            return Admin(*record[:7]) if len(record) >= 7 else Admin(record[0])
        return None

    def updatePersonalInfo(self, **kwargs):
        # Admin không cần cập nhật hồ sơ cá nhân trong phạm vi đặc tả
        return True, "Admin profile updated."

    # UC1: Tạo tài khoản mới cho sinh viên hoặc giảng viên
    def createAccount(self, userID, cccd, fullName, dob, email, gender,
                      phone, facultyCode, role, programID="", status="Active", intakeYear=""):
        # Tạo tài khoản mới, hệ thống tự sinh mật khẩu
        # Trả về (thành công, thông báo, mật khẩu được sinh)
        from models.account import Account
        from models.student import Student
        from models.lecturer import Lecturer
        from utils.validators import (validate_email, validate_phone,
                                       validate_not_empty, validate_date)

        # Kiểm tra các trường bắt buộc
        for val, name in [(userID, "ID"), (cccd, "National ID (CCCD)"),
                          (fullName, "Full Name"), (dob, "Date of Birth"),
                          (email, "Email"), (phone, "Phone"), (facultyCode, "Faculty")]:
            ok, msg = validate_not_empty(val, name)
            if not ok:
                return False, msg, ""
        if not validate_email(email):
            return False, "Invalid email format.", ""
        if not validate_phone(phone):
            return False, "Invalid phone number format.", ""
        ok, msg = validate_date(dob)
        if not ok:
            return False, msg, ""

        # Kiểm tra trùng lặp
        if find_record("accounts.txt", 0, userID):
            return False, f"ID '{userID}' already exists.", ""

        # Tạo tài khoản (mật khẩu tự sinh)
        account, raw_pwd, acc_msg = Account.create_new(userID, role, intakeYear)
        if not account:
            return False, acc_msg, ""

        # Tạo hồ sơ tương ứng theo vai trò
        if role == "Student":
            student = Student(userID, cccd, fullName, dob, email, gender,
                              phone, facultyCode, programID, status)
            student.save()
        elif role == "Lecturer":
            lecturer = Lecturer(userID, cccd, fullName, dob, email, gender,
                                phone, facultyCode)
            lecturer.save()

        return True, f"Account created. Username: {userID}", raw_pwd

    # UC8: Quản lý sinh viên (CRUD)
    def manageStudent(self, action, data=None):
        # hành động: 'list', 'add', 'update', 'delete'
        # data: dict chứa thông tin sinh viên hoặc student_id khi xóa
        from models.student import Student
        if action == "list":
            return True, Student.get_all()
        elif action == "add" and data:
            s = Student(**data)
            if Student.find_by_id(s.studentID):
                return False, f"Student ID '{s.studentID}' already exists."
            s.save()
            return True, "Student added successfully."
        elif action == "update" and data:
            s = Student(**data)
            s.save()
            return True, "Student updated successfully."
        elif action == "delete" and data:
            student_id = data if isinstance(data, str) else data.get("studentID", "")
            from models.account import Account
            from utils.file_handler import delete_record
            # Xóa cả tài khoản và hồ sơ sinh viên
            delete_record("accounts.txt", 0, student_id)
            delete_record("students.txt", 0, student_id)
            return True, "Student deleted successfully."
        return False, "Invalid action."

    # UC9: Quản lý giảng viên (CRUD)
    def manageLecturer(self, action, data=None):
        from models.lecturer import Lecturer
        if action == "list":
            return True, Lecturer.get_all()
        elif action == "add" and data:
            lec = Lecturer(**data)
            if Lecturer.find_by_id(lec.employeeID):
                return False, f"Employee ID '{lec.employeeID}' already exists."
            lec.save()
            return True, "Lecturer added successfully."
        elif action == "update" and data:
            lec = Lecturer(**data)
            lec.save()
            return True, "Lecturer updated successfully."
        elif action == "delete" and data:
            emp_id = data if isinstance(data, str) else data.get("employeeID", "")
            from utils.file_handler import delete_record
            # Xóa cả tài khoản và hồ sơ giảng viên
            delete_record("accounts.txt", 0, emp_id)
            delete_record("lecturers.txt", 0, emp_id)
            return True, "Lecturer deleted successfully."
        return False, "Invalid action."

    # UC11: Quản lý khoa (CRUD)
    def manageFaculty(self, action, data=None):
        from models.faculty import Faculty
        if action == "list":
            return True, Faculty.get_all()
        elif action == "add" and data:
            f = Faculty(**data)
            if Faculty.find_by_code(f.facultyCode):
                return False, f"Faculty code '{f.facultyCode}' already exists."
            f.save()
            return True, "Faculty added successfully."
        elif action == "update" and data:
            f = Faculty(**data)
            f.save()
            return True, "Faculty updated successfully."
        elif action == "delete" and data:
            code = data if isinstance(data, str) else data.get("facultyCode", "")
            from utils.file_handler import delete_record
            delete_record("faculties.txt", 0, code)
            return True, "Faculty deleted successfully."
        return False, "Invalid action."

    # UC12: Quản lý học kỳ (CRUD)
    def manageSemester(self, action, data=None):
        from models.semester import Semester
        import datetime
        if action == "list":
            return True, Semester.get_all()
        elif action == "add" and data:
            start = str(data.get("startDate", "")).strip()
            end = str(data.get("endDate", "")).strip()
            if start and end:
                try:
                    d_start = datetime.datetime.strptime(start, "%d/%m/%Y").date()
                    d_end = datetime.datetime.strptime(end, "%d/%m/%Y").date()
                    if d_end < d_start:
                        return False, "End date is invalid."
                except ValueError:
                    return False, "Date format is invalid."
            s = Semester(**data)
            if Semester.find_by_code(s.semester):
                return False, f"Semester '{s.semester}' already exists."
            s.save()
            return True, "Semester added successfully."
        elif action == "update" and data:
            start = str(data.get("startDate", "")).strip()
            end = str(data.get("endDate", "")).strip()
            if start and end:
                try:
                    d_start = datetime.datetime.strptime(start, "%d/%m/%Y").date()
                    d_end = datetime.datetime.strptime(end, "%d/%m/%Y").date()
                    if d_end < d_start:
                        return False, "End date is invalid."
                except ValueError:
                    return False, "Date format is invalid."
            s = Semester(**data)
            s.save()
            return True, "Semester updated successfully."
        elif action == "delete" and data:
            code = data if isinstance(data, str) else data.get("semester", "")
            from utils.file_handler import delete_record
            delete_record("semesters.txt", 0, code)
            return True, "Semester deleted successfully."
        return False, "Invalid action."

    # UC13: Quản lý môn học (CRUD)
    def manageCourse(self, action, data=None):
        from models.course import Course
        if action == "list":
            return True, Course.get_all()
        elif action == "add" and data:
            for field, field_name in [
                (data.get("courseCode", ""), "Course Code"),
                (data.get("courseName", ""), "Course Name"),
                (str(data.get("credits", "")), "Credits"),
                (data.get("facultyCode", ""), "Faculty Code"),
            ]:
                ok, msg = validate_not_empty(str(field), field_name)
                if not ok:
                    return False, msg

            ok, msg = validate_credits(str(data.get("credits", "")))
            if not ok:
                return False, msg

            c = Course(**data)
            if Course.find_by_code(c.courseCode):
                return False, f"Course code '{c.courseCode}' already exists."
            c.save()
            return True, "Course added successfully."
        elif action == "update" and data:
            if str(data.get("credits", "")).strip():
                ok, msg = validate_credits(str(data.get("credits", "")))
                if not ok:
                    return False, msg
            c = Course(**data)
            c.save()
            return True, "Course updated successfully."
        elif action == "delete" and data:
            code = data if isinstance(data, str) else data.get("courseCode", "")
            from utils.file_handler import delete_record
            delete_record("courses.txt", 0, code)
            return True, "Course deleted successfully."
        return False, "Invalid action."

    # UC14: Quản lý lớp học phần (CRUD)
    def manageClassSection(self, action, data=None):
        from models.class_section import ClassSection
        if action == "list":
            return True, ClassSection.get_all()
        elif action == "add" and data:
            cs = ClassSection(**data)
            if ClassSection.find_by_code(cs.classCode):
                return False, f"Class code '{cs.classCode}' already exists."
            cs.save()
            return True, "Class section added successfully."
        elif action == "update" and data:
            cs = ClassSection(**data)
            cs.save()
            return True, "Class section updated successfully."
        elif action == "delete" and data:
            code = data if isinstance(data, str) else data.get("classCode", "")
            from utils.file_handler import delete_record
            delete_record("classes.txt", 0, code)
            return True, "Class section deleted successfully."
        return False, "Invalid action."

    # UC10: Phân công giảng viên cho lớp học phần
    def assignLecturer(self, lecturerID, classCode):
        from models.lecturer import Lecturer
        from models.class_section import ClassSection
        lecturer = Lecturer.find_by_id(lecturerID)
        if not lecturer:
            return False, "Lecturer not found."
        cs = ClassSection.find_by_code(classCode)
        if not cs:
            return False, "Class section not found."
        cs._lecturerID = lecturerID
        cs.save()
        return True, f"Lecturer '{lecturerID}' assigned to class '{classCode}'."

    # UC18: Duyệt điểm (Finalize Grades)
    def finalizeGrades(self, classCode):
        # Duyệt tất cả điểm nháp (Draft) cho một lớp học phần
        # Khóa điểm vĩnh viễn, tính GPA cho sinh viên liên quan
        from models.grade import Grade
        from models.class_section import ClassSection
        from models.semester import Semester
        import datetime

        cs = ClassSection.find_by_code(classCode)
        if not cs:
            return False, "Class section not found."

        # Kiểm tra thời hạn chấm điểm (ngày kết thúc học kỳ)
        sem = Semester.find_by_code(cs.semesterCode)
        if sem:
            try:
                end = datetime.datetime.strptime(sem.endDate, "%d/%m/%Y").date()
                if datetime.date.today() < end:
                    return False, "Grading deadline has not passed yet."
            except ValueError:
                pass  # Nếu parse ngày lỗi, cho phép duyệt

        grades = Grade.find_by_class(classCode)
        draft_grades = [g for g in grades if g.status == "Draft"]
        if not draft_grades:
            return False, "No draft grades to finalize."

        # Duyệt từng bản ghi điểm nháp
        for g in draft_grades:
            g.finalize()

        # Tính lại GPA cho các sinh viên bị ảnh hưởng
        from models.student import Student
        student_ids = set(g.studentID for g in draft_grades)
        for sid in student_ids:
            student = Student.find_by_id(sid)
            if student:
                student.calculateSemesterGPA(cs.semesterCode)
                student.calculateCumulativeGPA()

        return True, f"Grades for class '{classCode}' have been finalized."

