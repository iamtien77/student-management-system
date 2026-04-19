"""
controllers/user_controller.py
xu ly cac luong nghiep vu quan ly tai khoan nguoi dung:
- tao tai khoan moi kem thong tin profile
- lay thong tin user record tuong ung voi tai khoan
"""

from models.account import Account
from models.student import Student
from models.lecturer import Lecturer
from utils.validators import is_valid_password, is_valid_email, is_not_empty


class UserController:
    """
    bo dieu khien quan ly nguoi dung
    duoc Admin su dung de tao tai khoan moi cho sinh vien / giang vien
    """

    @staticmethod
    def create_account(form_data: dict) -> tuple:
        """
        tao tai khoan moi:
        1. kiem tra du lieu dau vao
        2. kiem tra tai khoan da ton tai chua
        3. tao ban ghi nguoi dung (Student hoac Lecturer) roi moi tao Account
        tra ve (True, "") hoac (False, thong_bao_loi)
        """
        # lay du lieu tu form
        username    = form_data.get("username", "").strip()
        password    = form_data.get("password", "").strip()
        role        = form_data.get("role", "").strip()
        intake_year = form_data.get("intake_year", "").strip()
        full_name   = form_data.get("full_name", "").strip()
        email       = form_data.get("email", "").strip()
        cccd        = form_data.get("cccd", "").strip()
        dob         = form_data.get("dob", "").strip()
        gender      = form_data.get("gender", "").strip()
        phone       = form_data.get("phone", "").strip()

        # kiem tra cac truong bat buoc
        required = [username, password, role, full_name, email, cccd]
        if not all(is_not_empty(v) for v in required):
            return False, "Vui long nhap day du cac truong bat buoc"

        if not is_valid_email(email):
            return False, "Dinh dang email khong hop le"

        valid_pwd, msg = is_valid_password(password)
        if not valid_pwd:
            return False, msg

        # kiem tra tai khoan ton tai
        if Account.findById(username):
            return False, f"Ten dang nhap '{username}' da ton tai"

        # tao user_record tuong ung voi vai tro
        if role == "student":
            program_id = form_data.get("program_id", "UNKNOWN").strip()
            user_record = Student(
                cccd=cccd, fullName=full_name, dob=dob,
                email=email, gender=gender, phoneNumber=phone,
                studentID=username, programID=program_id, status="active"
            )
            user_record.save()

        elif role == "lecturer":
            user_record = Lecturer(
                cccd=cccd, fullName=full_name, dob=dob,
                email=email, gender=gender, phoneNumber=phone,
                employeeID=username
            )
            user_record.save()

        else:
            user_record = None  # admin khong co profile rieng trong luon nay

        # tao Account va luu xuong file
        account = Account(
            username=username,
            password=password,
            role=role,
            intakeYear=intake_year,
            userRecord=user_record
        )
        account.save()
        return True, f"Tao tai khoan '{username}' thanh cong"

    @staticmethod
    def get_user_record(account: Account):
        """
        lay thong tin user record tuong ung voi tai khoan dang dang nhap
        tra ve Student hoac Lecturer tuy theo vai tro
        """
        role     = account.getRole()
        username = account.getUsername()

        if role == "student":
            return Student.findById(username)
        elif role == "lecturer":
            return Lecturer.findById(username)
        return None
