# Lớp Faculty (Khoa) - Ánh xạ tới D3 (Kho dữ liệu Khoa)
# Thuộc tính: facultyCode, facultyName, email, phoneNumber
# Không có phương thức nghiệp vụ trong Class Diagram

from utils.file_handler import read_records, find_record, update_record, append_line, delete_record


class Faculty:
    # Tên file lưu trữ dữ liệu khoa
    FILE = "faculties.txt"

    def __init__(self, facultyCode, facultyName="", email="", phoneNumber=""):
        self._facultyCode = facultyCode   # Mã khoa
        self._facultyName = facultyName   # Tên khoa
        self._email = email               # Email liên hệ
        self._phoneNumber = phoneNumber   # Số điện thoại

    @property
    def facultyCode(self):
        return self._facultyCode

    @property
    def facultyName(self):
        return self._facultyName

    @property
    def email(self):
        return self._email

    @property
    def phoneNumber(self):
        return self._phoneNumber

    def to_record(self):
        return [self._facultyCode, self._facultyName, self._email, self._phoneNumber]

    @staticmethod
    def from_record(record):
        if len(record) >= 4:
            return Faculty(*record[:4])
        return None

    def save(self):
        # Lưu hoặc cập nhật bản ghi khoa
        if find_record(self.FILE, 0, self._facultyCode):
            return update_record(self.FILE, 0, self._facultyCode, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    def delete(self):
        return delete_record(self.FILE, 0, self._facultyCode)

    @staticmethod
    def find_by_code(code):
        # Tìm khoa theo mã
        record = find_record(Faculty.FILE, 0, code)
        return Faculty.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả các khoa
        return [Faculty.from_record(r) for r in read_records(Faculty.FILE)
                if Faculty.from_record(r) is not None]
