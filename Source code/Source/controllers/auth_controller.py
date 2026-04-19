"""
Bộ điều khiển xác thực
Xử lý: Đăng nhập (UC2), Quên mật khẩu (UC3), Đăng xuất (UC4), Đổi mật khẩu (UC5).
"""
from utils.file_handler import read_records, write_records, find_record, update_record
from utils.auth_helper import hash_password, verify_password, generate_password
from utils.validators import validate_password_complexity


# Lưu trữ phiên đăng nhập
_current_session = {"username": None, "role": None}


def get_session():
    return _current_session.copy()


def login(username, password):
    """
    UC2: Đăng nhập - kiểm tra thông tin xác thực, nhận diện vai trò.
    Trả về (thành_công, vai_trò_hoặc_lỗi).
    """
    record = find_record("accounts.txt", 0, username)
    if not record:
        return False, "Username does not exist."
    if len(record) < 3:
        return False, "Account data is corrupted."
    stored_hash = record[1]
    role = record[2]
    if not verify_password(password, stored_hash):
        return False, "Incorrect password."
    _current_session["username"] = username
    _current_session["role"] = role
    return True, role


def logout():
    """UC4: Đăng xuất - xóa phiên đăng nhập."""
    _current_session["username"] = None
    _current_session["role"] = None


def forgot_password(identifier):
    """
    UC3: Quên mật khẩu - tìm tài khoản theo email hoặc số điện thoại.
    Trả về (thành_công, tên_đăng_nhập_hoặc_lỗi).
    """
    # Tìm trong danh sách sinh viên
    from utils.file_handler import read_records
    for r in read_records("students.txt"):
        if len(r) >= 7 and (r[4].strip() == identifier.strip() or r[6].strip() == identifier.strip()):
            return True, r[0]  # student_id là tên đăng nhập
    # Tìm trong danh sách giảng viên
    for r in read_records("lecturers.txt"):
        if len(r) >= 7 and (r[4].strip() == identifier.strip() or r[6].strip() == identifier.strip()):
            return True, r[0]  # employee_id là tên đăng nhập
    return False, "No account found with this Email or Phone number."


def reset_password(username, new_password):
    """Đặt mật khẩu mới cho người dùng (dùng sau khi xác minh quên mật khẩu)."""
    valid, msg = validate_password_complexity(new_password)
    if not valid:
        return False, msg
    new_hash = hash_password(new_password)
    record = find_record("accounts.txt", 0, username)
    if not record:
        return False, "Account not found."
    record[1] = new_hash
    if update_record("accounts.txt", 0, username, record):
        return True, "Password reset successfully."
    return False, "Failed to update password."


def change_password(username, old_password, new_password, confirm_password):
    """
    UC5: Đổi mật khẩu - xác minh mật khẩu cũ, kiểm tra mật khẩu mới, rồi cập nhật.
    """
    if new_password != confirm_password:
        return False, "New passwords do not match."
    record = find_record("accounts.txt", 0, username)
    if not record:
        return False, "Account not found."
    if not verify_password(old_password, record[1]):
        return False, "Current password is incorrect."
    valid, msg = validate_password_complexity(new_password)
    if not valid:
        return False, msg
    record[1] = hash_password(new_password)
    if update_record("accounts.txt", 0, username, record):
        return True, "Password changed successfully."
    return False, "Failed to save new password."

