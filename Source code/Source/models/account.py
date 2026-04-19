# Lớp Account (Tài khoản) - Ánh xạ tới D1 (Kho dữ liệu Tài khoản)
# Xử lý xác thực: đăng nhập, đăng xuất, đổi mật khẩu, quên mật khẩu, đặt lại mật khẩu
# Thuộc tính: username, password, role, intakeYear

from utils.file_handler import read_records, write_records, find_record, update_record, append_line
from utils.auth_helper import hash_password, verify_password, generate_password
from utils.validators import validate_password_complexity


class Account:
    FILE = "accounts.txt"           # File lưu trữ tài khoản
    _current_session = None         # Phiên đăng nhập hiện tại

    def __init__(self, username, password, role, intakeYear=""):
        self._username = username
        self._password = password    # Lưu dạng băm (hash)
        self._role = role
        self._intakeYear = intakeYear

    # Thuộc tính

    @property
    def username(self):
        return self._username

    @property
    def role(self):
        return self._role

    @property
    def intakeYear(self):
        return self._intakeYear

    # Chuyển đổi dữ liệu

    def to_record(self):
        return [self._username, self._password, self._role, self._intakeYear]

    @staticmethod
    def from_record(record):
        # Tạo đối tượng Account từ bản ghi file
        if len(record) >= 3:
            return Account(
                record[0], record[1], record[2],
                record[3] if len(record) > 3 else ""
            )
        return None

    # Phương thức theo Class Diagram

    @staticmethod
    def login(username, password):
        # UC2: Đăng nhập - xác thực tên đăng nhập và mật khẩu
        record = find_record(Account.FILE, 0, username)
        if not record:
            return False, "Username does not exist."
        if len(record) < 3:
            return False, "Account data is corrupted."

        if not verify_password(password, record[1]):
            return False, "Incorrect password."

        # Tạo phiên đăng nhập
        account = Account.from_record(record)
        Account._current_session = account
        return True, account

    def logout(self):
        # UC4: Đăng xuất - xóa phiên làm việc
        Account._current_session = None

    def changePassword(self, oldPwd, newPwd):
        # UC5: Đổi mật khẩu sau khi xác minh mật khẩu cũ
        if not verify_password(oldPwd, self._password):
            return False, "Current password is incorrect."
        valid, msg = validate_password_complexity(newPwd)
        if not valid:
            return False, msg
        self._password = hash_password(newPwd)
        if update_record(self.FILE, 0, self._username, self.to_record()):
            return True, "Password changed successfully."
        return False, "Failed to save new password."

    @staticmethod
    def forgotPassword(email):
        # UC3 bước 1: Tìm tài khoản qua email hoặc số điện thoại
        for r in read_records("students.txt"):
            if len(r) >= 7:
                if r[4].strip() == email.strip() or r[6].strip() == email.strip():
                    return True, r[0]
        for r in read_records("lecturers.txt"):
            if len(r) >= 7:
                if r[4].strip() == email.strip() or r[6].strip() == email.strip():
                    return True, r[0]
        return False, "No account found with this Email or Phone number."

    def resetPassword(self, newPwd):
        # UC3 bước 2: Đặt lại mật khẩu mới sau xác minh
        valid, msg = validate_password_complexity(newPwd)
        if not valid:
            return False, msg
        self._password = hash_password(newPwd)
        if update_record(self.FILE, 0, self._username, self.to_record()):
            return True, "Password reset successfully."
        return False, "Failed to reset password."

    # Phương thức hỗ trợ

    @staticmethod
    def get_current_session():
        return Account._current_session

    @staticmethod
    def find_by_username(username):
        # Tìm tài khoản theo tên đăng nhập
        record = find_record(Account.FILE, 0, username)
        return Account.from_record(record) if record else None

    def save(self):
        # Lưu tài khoản vào file (thêm mới)
        return append_line(self.FILE, "|".join(self.to_record()))

    @staticmethod
    def create_new(username, role, intakeYear=""):
        # Tạo tài khoản mới với mật khẩu tự sinh
        if find_record(Account.FILE, 0, username):
            return None, "", "Username already exists."
        raw_pwd = generate_password()
        hashed = hash_password(raw_pwd)
        account = Account(username, hashed, role, intakeYear)
        account.save()
        return account, raw_pwd, "Account created successfully."
