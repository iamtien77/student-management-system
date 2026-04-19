# Lớp trừu tượng UserRecord (Hồ sơ Người dùng)
# Lớp cha cho Student, Lecturer, Admin
# Chứa các trường thông tin cá nhân chung: CCCD, fullName, DOB, email, gender, phoneNumber

from abc import ABC, abstractmethod


class UserRecord(ABC):
    # Lớp cơ sở trừu tượng đại diện cho hồ sơ cá nhân của người dùng

    def __init__(self, cccd, fullName, dob, email, gender, phoneNumber):
        self._cccd = cccd               # Căn cước công dân
        self._fullName = fullName       # Họ và tên
        self._dob = dob                 # Ngày sinh (DD/MM/YYYY)
        self._email = email             # Email
        self._gender = gender           # Giới tính
        self._phoneNumber = phoneNumber # Số điện thoại

    # Thuộc tính

    @property
    def cccd(self):
        return self._cccd

    @property
    def fullName(self):
        return self._fullName

    @property
    def dob(self):
        return self._dob

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def gender(self):
        return self._gender

    @property
    def phoneNumber(self):
        return self._phoneNumber

    @phoneNumber.setter
    def phoneNumber(self, value):
        self._phoneNumber = value

    # Phương thức trừu tượng - lớp con phải triển khai

    @abstractmethod
    def updatePersonalInfo(self, **kwargs):
        # UC7: Cập nhật thông tin cá nhân
        # Mỗi vai trò có quyền sửa khác nhau
        pass

    @abstractmethod
    def to_record(self):
        # Chuyển đối tượng thành danh sách trường để lưu file
        pass

    @staticmethod
    @abstractmethod
    def from_record(record):
        # Tạo đối tượng từ bản ghi file
        pass
