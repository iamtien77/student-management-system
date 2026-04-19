"""
utils/auth_helper.py
cac tien ich lien quan den xac thuc nguoi dung:
- bam (hash) mat khau bang SHA-256
- sinh mat khau ngau nhien tam thoi
"""

import hashlib
import random
import string


def hash_password(password: str) -> str:
    """bam mat khau bang SHA-256, tra ve chuoi hex 64 ky tu"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """so sanh mat khau nguoi dung nhap vao voi ban bam da luu"""
    return hash_password(plain_password) == hashed_password


def generate_temp_password(length: int = 10) -> str:
    """
    sinh mat khau tam thoi ngau nhien dam bao:
    - co chu hoa, chu thuong, so va ky tu dac biet
    dung khi admin reset mat khau cho nguoi dung
    """
    uppercase   = random.choices(string.ascii_uppercase, k=2)
    lowercase   = random.choices(string.ascii_lowercase, k=4)
    digits      = random.choices(string.digits, k=2)
    special     = random.choices("!@#$%^&*()", k=2)
    all_chars   = uppercase + lowercase + digits + special
    random.shuffle(all_chars)
    return "".join(all_chars)
