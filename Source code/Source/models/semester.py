# Lớp Semester (Học kỳ) - Ánh xạ tới D4 (Kho dữ liệu Học kỳ)
# Thuộc tính: semester, startDate, endDate, examWeeks

from utils.file_handler import read_records, find_record, update_record, append_line, delete_record


class Semester:
    # Tên file lưu trữ dữ liệu học kỳ
    FILE = "semesters.txt"

    def __init__(self, semester, startDate="", endDate="", examWeeks=""):
        self._semester = semester       # Mã học kỳ (ví dụ: HK1_2025)
        self._startDate = startDate     # Ngày bắt đầu (DD/MM/YYYY)
        self._endDate = endDate         # Ngày kết thúc (DD/MM/YYYY)
        self._examWeeks = examWeeks     # Tuần thi (khoảng ngày)

    @property
    def semester(self):
        return self._semester

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate

    @property
    def examWeeks(self):
        return self._examWeeks

    def to_record(self):
        return [self._semester, self._startDate, self._endDate, self._examWeeks]

    @staticmethod
    def from_record(record):
        if len(record) >= 4:
            return Semester(*record[:4])
        return None

    def save(self):
        # Lưu hoặc cập nhật bản ghi học kỳ
        if find_record(self.FILE, 0, self._semester):
            return update_record(self.FILE, 0, self._semester, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    def delete(self):
        return delete_record(self.FILE, 0, self._semester)

    @staticmethod
    def find_by_code(code):
        # Tìm học kỳ theo mã
        record = find_record(Semester.FILE, 0, code)
        return Semester.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả học kỳ
        return [Semester.from_record(r) for r in read_records(Semester.FILE)
                if Semester.from_record(r) is not None]
