"""
Hệ thống Quản lý Sinh viên - Điểm vào chính của Ứng dụng
Triển khai bộ điều khiển ứng dụng quản lý điều hướng giữa các giao diện.
"""
import sys
import os
import tkinter as tk

# Thêm thư mục Source vào đường dẫn hệ thống
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.account import Account
from models.admin import Admin
from views.base_view import COLORS


class Application:
    """Bộ điều khiển ứng dụng chính - quản lý điều hướng giao diện và phiên đăng nhập."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Management System")
        self.root.configure(bg=COLORS["bg"])
        self._account = None
        self._init_default_admin()
        self._show_login()

    def _init_default_admin(self):
        """Đảm bảo tài khoản admin mặc định tồn tại."""
        if not Account.find_by_username("iamtien"):
            from utils.auth_helper import hash_password
            from utils.file_handler import append_line
            append_line("accounts.txt", f"iamtien|{hash_password('Tien77@')}|Admin|")
            print("[System] Default admin created. Username: iamtien | Password: Tien77@")

    # ---- Điều hướng ----
    def _show_login(self):
        self._account = None
        Account._current_session = None
        from views.auth.login_view import LoginView
        view = LoginView(self.root, self._on_login_success, self._show_forgot_password)
        view.show()

    def _show_forgot_password(self):
        from views.auth.forgot_password_view import ForgotPasswordView
        view = ForgotPasswordView(self.root, self._show_login)
        view.show()

    def _on_login_success(self, account):
        self._account = account
        role = account.role
        if role == "Admin":
            self._show_admin_dashboard()
        elif role == "Student":
            self._show_student_dashboard()
        elif role == "Lecturer":
            self._show_lecturer_dashboard()

    # ---- Điều hướng Admin ----
    def _show_admin_dashboard(self):
        from views.admin.dashboard import AdminDashboard
        view = AdminDashboard(self.root, self._account, self._admin_navigate)
        view.show()

    def _admin_navigate(self, view_name):
        if view_name == "logout":
            self._show_login()
        elif view_name == "dashboard":
            self._show_admin_dashboard()
        elif view_name == "change_password":
            from views.shared.change_password_view import ChangePasswordView
            ChangePasswordView(self.root, self._account, self._admin_navigate).show()
        elif view_name == "create_account":
            from views.admin.create_account_view import CreateAccountView
            CreateAccountView(self.root, self._account, self._admin_navigate).show()
        elif view_name == "manage_student":
            self._show_crud("Manage Student Profile", self._student_crud_config())
        elif view_name == "manage_lecturer":
            self._show_crud("Manage Lecturer Profile", self._lecturer_crud_config())
        elif view_name == "manage_faculty":
            self._show_crud("Manage Faculty", self._faculty_crud_config())
        elif view_name == "manage_semester":
            self._show_crud("Manage Semester", self._semester_crud_config())
        elif view_name == "manage_course":
            self._show_crud("Manage Course", self._course_crud_config())
        elif view_name == "manage_class":
            self._show_crud("Manage Class Section", self._class_crud_config())
        elif view_name == "assign_lecturer":
            from views.admin.assign_lecturer_view import AssignLecturerView
            AssignLecturerView(self.root, self._account, self._admin_navigate).show()
        elif view_name == "finalize_grades":
            from views.admin.finalize_grades_view import FinalizeGradesView
            FinalizeGradesView(self.root, self._account, self._admin_navigate).show()

    def _show_crud(self, title, config):
        config['title'] = title
        from views.components.crud_view import CrudView
        CrudView(self.root, self._account, self._admin_navigate, config).show()

    # ---- Điều hướng Sinh viên ----
    def _show_student_dashboard(self):
        from views.student.dashboard import StudentDashboard
        StudentDashboard(self.root, self._account, self._student_navigate).show()

    def _student_navigate(self, view_name):
        if view_name == "logout":
            self._show_login()
        elif view_name == "dashboard":
            self._show_student_dashboard()
        elif view_name == "change_password":
            from views.shared.change_password_view import ChangePasswordView
            ChangePasswordView(self.root, self._account, self._student_navigate).show()
        elif view_name == "view_profile":
            from views.shared.profile_view import ProfileView
            ProfileView(self.root, self._account, self._student_navigate, "view").show()
        elif view_name == "update_profile":
            from views.shared.profile_view import ProfileView
            ProfileView(self.root, self._account, self._student_navigate, "update").show()
        elif view_name == "training_program":
            from views.student.training_program_view import TrainingProgramView
            TrainingProgramView(self.root, self._account, self._student_navigate).show()
        elif view_name == "view_grades":
            from views.student.view_grades_view import ViewGradesView
            ViewGradesView(self.root, self._account, self._student_navigate).show()
    # ---- Điều hướng Giảng viên ----
    def _show_lecturer_dashboard(self):
        from views.lecturer.dashboard import LecturerDashboard
        LecturerDashboard(self.root, self._account, self._lecturer_navigate).show()

    def _lecturer_navigate(self, view_name):
        if view_name == "logout":
            self._show_login()
        elif view_name == "dashboard":
            self._show_lecturer_dashboard()
        elif view_name == "change_password":
            from views.shared.change_password_view import ChangePasswordView
            ChangePasswordView(self.root, self._account, self._lecturer_navigate).show()
        elif view_name == "view_profile":
            from views.shared.profile_view import ProfileView
            ProfileView(self.root, self._account, self._lecturer_navigate, "view").show()
        elif view_name == "update_profile":
            from views.shared.profile_view import ProfileView
            ProfileView(self.root, self._account, self._lecturer_navigate, "update").show()
        elif view_name == "attendance":
            from views.lecturer.attendance_view import AttendanceView
            AttendanceView(self.root, self._account, self._lecturer_navigate).show()
        elif view_name == "enter_grades":
            from views.lecturer.enter_grades_view import EnterGradesView
            EnterGradesView(self.root, self._account, self._lecturer_navigate).show()

    # ---- Cấu hình CRUD ----
    def _student_crud_config(self):
        from models.student import Student
        admin = Admin(self._account.username)
        return {
            'columns': [
                ("studentID", "Student ID", 100), ("cccd", "CCCD", 100),
                ("fullName", "Full Name", 150), ("dob", "DOB", 90),
                ("email", "Email", 150), ("gender", "Gender", 70),
                ("phoneNumber", "Phone", 110), ("facultyCode", "Faculty", 80),
                ("programID", "Program", 80), ("status", "Status", 80),
            ],
            'fields': [
                ("studentID", "Student ID", False), ("cccd", "National ID (CCCD)", True),
                ("fullName", "Full Name", True), ("dob", "Date of Birth", True),
                ("email", "Email", True), ("gender", "Gender", True),
                ("phoneNumber", "Phone Number", True), ("facultyCode", "Faculty Code", True),
                ("programID", "Program ID", True), ("status", "Status", True),
            ],
            'get_all': lambda: [s.to_record() for s in Student.get_all()],
            'add': lambda d: admin.manageStudent("add", d),
            'update': lambda d: admin.manageStudent("update", d),
            'delete': lambda k: admin.manageStudent("delete", k),
            'key_field': "studentID",
        }

    def _lecturer_crud_config(self):
        from models.lecturer import Lecturer
        admin = Admin(self._account.username)
        return {
            'columns': [
                ("employeeID", "Employee ID", 100), ("cccd", "CCCD", 100),
                ("fullName", "Full Name", 150), ("dob", "DOB", 90),
                ("email", "Email", 150), ("gender", "Gender", 70),
                ("phoneNumber", "Phone", 110), ("facultyCode", "Faculty", 80),
            ],
            'fields': [
                ("employeeID", "Employee ID", False), ("cccd", "National ID (CCCD)", True),
                ("fullName", "Full Name", True), ("dob", "Date of Birth", True),
                ("email", "Email", True), ("gender", "Gender", True),
                ("phoneNumber", "Phone Number", True), ("facultyCode", "Faculty Code", True),
            ],
            'get_all': lambda: [l.to_record() for l in Lecturer.get_all()],
            'add': lambda d: admin.manageLecturer("add", d),
            'update': lambda d: admin.manageLecturer("update", d),
            'delete': lambda k: admin.manageLecturer("delete", k),
            'key_field': "employeeID",
        }

    def _faculty_crud_config(self):
        from models.faculty import Faculty
        admin = Admin(self._account.username)
        return {
            'columns': [
                ("facultyCode", "Faculty Code", 120), ("facultyName", "Faculty Name", 250),
                ("email", "Email", 200), ("phoneNumber", "Phone", 150),
            ],
            'fields': [
                ("facultyCode", "Faculty Code", False), ("facultyName", "Faculty Name", True),
                ("email", "Email", True), ("phoneNumber", "Phone Number", True),
            ],
            'get_all': lambda: [f.to_record() for f in Faculty.get_all()],
            'add': lambda d: admin.manageFaculty("add", d),
            'update': lambda d: admin.manageFaculty("update", d),
            'delete': lambda k: admin.manageFaculty("delete", k),
            'key_field': "facultyCode",
        }

    def _semester_crud_config(self):
        from models.semester import Semester
        admin = Admin(self._account.username)
        return {
            'columns': [
                ("semester", "Semester Code", 150), ("startDate", "Start Date", 120),
                ("endDate", "End Date", 120), ("examWeeks", "Exam Weeks", 200),
            ],
            'fields': [
                ("semester", "Semester Code", False), ("startDate", "Start Date (DD/MM/YYYY)", True),
                ("endDate", "End Date (DD/MM/YYYY)", True), ("examWeeks", "Exam Weeks", True),
            ],
            'get_all': lambda: [s.to_record() for s in Semester.get_all()],
            'add': lambda d: admin.manageSemester("add", d),
            'update': lambda d: admin.manageSemester("update", d),
            'delete': lambda k: admin.manageSemester("delete", k),
            'key_field': "semester",
        }

    def _course_crud_config(self):
        from models.course import Course
        admin = Admin(self._account.username)
        return {
            'columns': [
                ("courseCode", "Course Code", 110), ("courseName", "Course Name", 200),
                ("credits", "Credits", 70), ("facultyCode", "Faculty", 100),
                ("prerequisites", "Prerequisites", 200),
            ],
            'fields': [
                ("courseCode", "Course Code", False), ("courseName", "Course Name", True),
                ("credits", "Credits", True), ("facultyCode", "Faculty Code", True),
                ("prerequisites", "Prerequisites (comma-separated)", True),
            ],
            'get_all': lambda: [c.to_record() for c in Course.get_all()],
            'add': lambda d: admin.manageCourse("add", d),
            'update': lambda d: admin.manageCourse("update", d),
            'delete': lambda k: admin.manageCourse("delete", k),
            'key_field': "courseCode",
        }

    def _class_crud_config(self):
        from models.class_section import ClassSection
        admin = Admin(self._account.username)
        return {
            'columns': [
                ("classCode", "Class Code", 100), ("courseCode", "Course", 90),
                ("semesterCode", "Semester", 90), ("maxCapacity", "Max Cap.", 70),
                ("currentEnrollment", "Enrolled", 70), ("dayOfWeek", "Day", 80),
                ("startTime", "Start", 60), ("endTime", "End", 60),
                ("room", "Room", 60), ("lecturerID", "Lecturer", 90),
            ],
            'fields': [
                ("classCode", "Class Code", False), ("courseCode", "Course Code", True),
                ("semesterCode", "Semester Code", True), ("maxCapacity", "Max Capacity", True),
                ("currentEnrollment", "Current Enrollment", True),
                ("dayOfWeek", "Day of Week", True), ("startTime", "Start Time", True),
                ("endTime", "End Time", True), ("room", "Room", True),
                ("lecturerID", "Lecturer ID", True),
            ],
            'get_all': lambda: [cs.to_record() for cs in ClassSection.get_all()],
            'add': lambda d: admin.manageClassSection("add", d),
            'update': lambda d: admin.manageClassSection("update", d),
            'delete': lambda k: admin.manageClassSection("delete", k),
            'key_field': "classCode",
        }

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()
