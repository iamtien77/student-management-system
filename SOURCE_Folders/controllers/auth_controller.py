"""
controllers/auth_controller.py
xu ly cac luong nghiep vu lien quan den xac thuc:
- dang nhap: kiem tra tai khoan, phan loai vai tro
- doi mat khau: xac thuc mat khau cu truoc khi cho thay doi
- quen mat khau: xac minh email roi dat lai mat khau
"""

from models.account import Account
from utils.validators import is_valid_password, is_valid_email


class AuthController:
    """
    bo dieu khien xac thuc
    khong chua bat ky code giao dien nao, chi xu ly logic va tra ve ket qua
    """

    @staticmethod
    def login(username: str, password: str) -> tuple:
        """
        kiem tra thong tin dang nhap
        tra ve (account, "") neu thanh cong
        tra ve (None, thong_bao_loi) neu that bai
        """
        if not username.strip() or not password.strip():
            return None, "Vui long nhap day du ten dang nhap va mat khau"

        account = Account.findById(username.strip())
        if account is None:
            return None, "Ten dang nhap khong ton tai"

        # su dung phuong thuc login cua model de kiem tra mat khau
        if not account.login(username.strip(), password):
            return None, "Mat khau khong chinh xac"

        return account, ""

    @staticmethod
    def change_password(account: Account, old_pwd: str, new_pwd: str) -> tuple:
        """
        doi mat khau:
        1. kiem tra mat khau cu
        2. kiem tra do manh mat khau moi
        3. luu lai neu hop le
        """
        if not old_pwd or not new_pwd:
            return False, "Vui long nhap day du thong tin"

        valid, msg = is_valid_password(new_pwd)
        if not valid:
            return False, msg

        try:
            result = account.changePassword(old_pwd, new_pwd)
            if result:
                return True, "Doi mat khau thanh cong"
            return False, "Mat khau cu khong dung"
        except ValueError as e:
            return False, str(e)

    @staticmethod
    def reset_password(account: Account, new_pwd: str) -> tuple:
        """
        dat lai mat khau (khi admin reset hoac sau khi xac minh email)
        """
        valid, msg = is_valid_password(new_pwd)
        if not valid:
            return False, msg
        try:
            account.resetPassword(new_pwd)
            return True, "Dat lai mat khau thanh cong"
        except ValueError as e:
            return False, str(e)

    @staticmethod
    def verify_email_for_reset(username: str, email: str) -> tuple:
        """
        xac minh email khi nguoi dung quen mat khau
        tra ve (account, "") neu email khop
        tra ve (None, loi) neu khong khop
        """
        if not is_valid_email(email):
            return None, "Dinh dang email khong hop le"

        account = Account.findById(username.strip())
        if account is None:
            return None, "Ten dang nhap khong ton tai"

        try:
            account.forgotPassword(email.strip())
            return account, ""
        except ValueError as e:
            return None, str(e)
