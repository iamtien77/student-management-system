"""
Mô-đun Kiểm tra Dữ liệu Đầu vào (Validators)
Cung cấp các hàm kiểm tra định dạng: email, số điện thoại,
độ phức tạp mật khẩu, trường bắt buộc, ngày tháng, tín chỉ, điểm số.
"""
import re


def validate_email(email):
    """
    Kiểm tra định dạng email hợp lệ.
    Ví dụ hợp lệ: student@university.edu.vn
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Kiểm tra số điện thoại hợp lệ (Việt Nam).
    Yêu cầu: bắt đầu bằng 0, có 10-11 chữ số.
    """
    pattern = r'^0\d{9,10}$'
    return bool(re.match(pattern, phone))


def validate_password_complexity(password):
    """
    Kiểm tra độ phức tạp mật khẩu theo yêu cầu đặc tả:
    - Tối thiểu 8 ký tự
    - Có ít nhất 1 chữ hoa
    - Có ít nhất 1 chữ số
    - Có ít nhất 1 ký tự đặc biệt
    Trả về (hợp_lệ: bool, thông_báo_lỗi: str).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, ""


def validate_not_empty(value, field_name="Field"):
    """Kiểm tra giá trị không được để trống."""
    if not value or not value.strip():
        return False, f"{field_name} must not be empty."
    return True, ""


def validate_date(date_str):
    """
    Kiểm tra định dạng ngày tháng DD/MM/YYYY.
    Đảm bảo ngày, tháng, năm nằm trong khoảng hợp lệ.
    """
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(pattern, date_str):
        return False, "Date must be in DD/MM/YYYY format."
    try:
        d, m, y = int(date_str[:2]), int(date_str[3:5]), int(date_str[6:])
        if m < 1 or m > 12 or d < 1 or d > 31 or y < 1900:
            return False, "The date value is invalid."
    except ValueError:
        return False, "Invalid date format."
    return True, ""


def validate_credits(credits_str):
    """Kiểm tra số tín chỉ phải là số nguyên dương."""
    try:
        c = int(credits_str)
        if c <= 0:
            return False, "Credits must be a positive number."
        return True, ""
    except ValueError:
        return False, "Credits must be a number."


def validate_grade(grade_str):
    """Kiểm tra điểm số phải là số thực trong khoảng 0 đến 10."""
    try:
        g = float(grade_str)
        if g < 0 or g > 10:
            return False, "Grade must be between 0 and 10."
        return True, ""
    except ValueError:
        return False, "Grade must be a number."
