"""
Bộ điều khiển người dùng
Xử lý: Tạo tài khoản (UC1), Xem/Cập nhật hồ sơ (UC6,7),
    Quản lý sinh viên (UC8), Quản lý giảng viên (UC9).
"""
from utils.file_handler import (read_records, write_records, find_record,
                                 append_line, update_record, delete_record)
from utils.auth_helper import hash_password, generate_password
from utils.validators import validate_email, validate_phone, validate_not_empty, validate_date


def create_account(user_id, cccd, full_name, dob, email, gender, phone, faculty, role,
                   major="", status="Active", actor_role=None):
    """
    UC1: Tạo tài khoản - Quản trị viên tạo tài khoản cho sinh viên/giảng viên.
    Tên đăng nhập = user_id. Mật khẩu = tạo tự động.
    Trả về (thành_công, thông_báo, mật_khẩu_được_tạo).
    """
    
    if actor_role != "Admin":
        return False, "Access denied. Only Admin can create accounts.", ""

    # Kiểm tra các trường bắt buộc
    for field, name in [(user_id, "ID"), (cccd, "National ID"), (full_name, "Full Name"),
                        (dob, "Date of Birth"), (email, "Email"), (phone, "Phone"), (faculty, "Faculty")]:
        ok, msg = validate_not_empty(field, name)
        if not ok:
            return False, msg, ""
    if not validate_email(email):
        return False, "Invalid email format.", ""
    if not validate_phone(phone):
        return False, "Invalid phone number format.", ""
    ok, msg = validate_date(dob)
    if not ok:
        return False, msg, ""

    # Kiểm tra mã bị trùng
    if find_record("accounts.txt", 0, user_id):
        return False, f"ID '{user_id}' already exists.", ""

    # Tạo mật khẩu
    raw_password = generate_password()
    hashed = hash_password(raw_password)

    # Lưu tài khoản
    account_role = "Student" if role == "Student" else "Lecturer"
    append_line("accounts.txt", f"{user_id}|{hashed}|{account_role}")

    # Lưu hồ sơ
    if role == "Student":
        append_line("students.txt",
                     f"{user_id}|{cccd}|{full_name}|{dob}|{email}|{gender}|{phone}|{faculty}|{major}|{status}")
    else:
        append_line("lecturers.txt",
                     f"{user_id}|{cccd}|{full_name}|{dob}|{email}|{gender}|{phone}|{faculty}")

    return True, f"Account created. Username: {user_id}", raw_password


# ---- Quản lý sinh viên (UC8) ----

def get_all_students():
    return read_records("students.txt")


def add_student(student_id, cccd, full_name, dob, email, gender, phone, faculty, major, status):
    if find_record("students.txt", 0, student_id):
        return False, f"Student ID '{student_id}' already exists."
    append_line("students.txt",
                f"{student_id}|{cccd}|{full_name}|{dob}|{email}|{gender}|{phone}|{faculty}|{major}|{status}")
    return True, "Student added successfully."


def update_student(student_id, new_data):
    """new_data là danh sách chứa toàn bộ trường dữ liệu."""
    return update_record("students.txt", 0, student_id, new_data), "Student updated."


def delete_student(student_id):
    # Đồng thời xóa tài khoản
    delete_record("accounts.txt", 0, student_id)
    return delete_record("students.txt", 0, student_id), "Student deleted."


def get_student(student_id):
    return find_record("students.txt", 0, student_id)


# ---- Quản lý giảng viên (UC9) ----

def get_all_lecturers():
    return read_records("lecturers.txt")


def add_lecturer(emp_id, cccd, full_name, dob, email, gender, phone, faculty):
    if find_record("lecturers.txt", 0, emp_id):
        return False, f"Employee ID '{emp_id}' already exists."
    append_line("lecturers.txt",
                f"{emp_id}|{cccd}|{full_name}|{dob}|{email}|{gender}|{phone}|{faculty}")
    return True, "Lecturer added successfully."


def update_lecturer(emp_id, new_data):
    return update_record("lecturers.txt", 0, emp_id, new_data), "Lecturer updated."


def delete_lecturer(emp_id):
    delete_record("accounts.txt", 0, emp_id)
    return delete_record("lecturers.txt", 0, emp_id), "Lecturer deleted."


def get_lecturer(emp_id):
    return find_record("lecturers.txt", 0, emp_id)


# ---- Hồ sơ cá nhân (UC6, UC7) ----

def get_profile(username, role):
    """UC6: Xem hồ sơ."""
    if role == "Student":
        return get_student(username)
    elif role == "Lecturer":
        return get_lecturer(username)
    return None


def update_profile(username, role, email, phone):
    """UC7: Cập nhật hồ sơ - chỉ cho phép sửa Email và Số điện thoại."""
    if not validate_email(email):
        return False, "Invalid email format."
    if not validate_phone(phone):
        return False, "Invalid phone number."

    if role == "Student":
        record = get_student(username)
        if record and len(record) >= 10:
            record[4] = email
            record[6] = phone
            update_record("students.txt", 0, username, record)
            return True, "Profile updated."
    elif role == "Lecturer":
        record = get_lecturer(username)
        if record and len(record) >= 8:
            record[4] = email
            record[6] = phone
            update_record("lecturers.txt", 0, username, record)
            return True, "Profile updated."
    return False, "Profile not found."

