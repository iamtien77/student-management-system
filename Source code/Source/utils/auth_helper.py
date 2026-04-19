# Mô-đun Hỗ trợ Xác thực (Auth Helper)
# Xử lý băm mật khẩu (SHA-256), tạo mật khẩu ngẫu nhiên và so sánh mật khẩu

import hashlib
import random
import string


def hash_password(password):
    # Băm mật khẩu bằng thuật toán SHA-256, trả về chuỗi hex
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password, hashed):
    # So sánh mật khẩu gốc với bản băm đã lưu
    return hash_password(password) == hashed


def generate_password(length=10):
    # Tạo mật khẩu ngẫu nhiên đáp ứng yêu cầu độ phức tạp:
    # Tối thiểu 8 ký tự, có chữ hoa, chữ thường, chữ số, ký tự đặc biệt
    if length < 8:
        length = 8
    # Đảm bảo có ít nhất 1 ký tự mỗi loại
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")
    # Phần còn lại chọn ngẫu nhiên
    rest = random.choices(
        string.ascii_letters + string.digits + "!@#$%^&*",
        k=length - 4
    )
    # Xáo trộn thứ tự
    password = list(upper + lower + digit + special + "".join(rest))
    random.shuffle(password)
    return "".join(password)
