"""
utils/validators.py
cac ham kiem tra tinh hop le (validation) dung chung toan bo he thong
khong import tkinter, khong phu thuoc vao view hay model
"""

import re


def is_valid_email(email: str) -> bool:
    """kiem tra email co dung dinh dang khong"""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email.strip()))


def is_valid_phone(phone: str) -> bool:
    """kiem tra so dien thoai Viet Nam (10-11 chu so, bat dau bang 0)"""
    pattern = r"^0\d{9,10}$"
    return bool(re.match(pattern, phone.strip()))


def is_valid_password(password: str) -> tuple:
    """
    kiem tra do manh cua mat khau:
    - it nhat 8 ky tu
    - co chu hoa
    - co chu so
    - co ky tu dac biet
    tra ve (True, "") neu hop le, (False, thong_bao_loi) neu khong
    """
    if len(password) < 8:
        return False, "Mat khau phai co it nhat 8 ky tu"
    if not re.search(r"[A-Z]", password):
        return False, "Mat khau phai co it nhat 1 chu hoa"
    if not re.search(r"[0-9]", password):
        return False, "Mat khau phai co it nhat 1 chu so"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Mat khau phai co it nhat 1 ky tu dac biet"
    return True, ""


def is_valid_date(date_str: str) -> bool:
    """kiem tra dinh dang ngay thang dd/mm/yyyy"""
    pattern = r"^\d{2}/\d{2}/\d{4}$"
    if not re.match(pattern, date_str.strip()):
        return False
    try:
        day, month, year = map(int, date_str.split("/"))
        return 1 <= day <= 31 and 1 <= month <= 12 and year >= 1900
    except ValueError:
        return False


def is_not_empty(value: str) -> bool:
    """kiem tra chuoi co khong rong khong"""
    return bool(value and value.strip())


def is_valid_cccd(cccd: str) -> bool:
    """kiem tra can cuoc cong dan Viet Nam (12 chu so)"""
    return bool(re.match(r"^\d{12}$", cccd.strip()))
