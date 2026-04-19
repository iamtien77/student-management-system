# Lớp Course (Môn học) - Ánh xạ tới D5 (Kho dữ liệu Môn học)
# Thuộc tính: courseCode, courseName, credits, prerequisites (tự tham chiếu)
# Quan hệ: thuộc quản lý bởi Faculty (managed by)

from utils.file_handler import read_records, find_record, update_record, append_line, delete_record


class Course:
    # Tên file lưu trữ dữ liệu môn học
    FILE = "courses.txt"

    def __init__(self, courseCode, courseName="", credits=0, facultyCode="", prerequisites=""):
        self._courseCode = courseCode       # Mã môn học
        self._courseName = courseName      # Tên môn học
        self._credits = int(credits) if credits else 0  # Số tín chỉ
        self._facultyCode = facultyCode    # Mã khoa quản lý (FK tới Faculty)
        # Danh sách môn tiên quyết lưu dạng chuỗi phân cách bởi dấu phẩy
        self._prerequisites = prerequisites

    @property
    def courseCode(self):
        return self._courseCode

    @property
    def courseName(self):
        return self._courseName

    @property
    def credits(self):
        return self._credits

    @property
    def facultyCode(self):
        return self._facultyCode

    @property
    def prerequisites(self):
        return self._prerequisites

    def get_prerequisite_list(self):
        # Trả về danh sách mã các môn tiên quyết
        if not self._prerequisites or self._prerequisites.strip() == "":
            return []
        return [c.strip() for c in self._prerequisites.split(",") if c.strip()]

    def to_record(self):
        return [self._courseCode, self._courseName, str(self._credits),
                self._facultyCode, self._prerequisites]

    @staticmethod
    def from_record(record):
        if len(record) >= 5:
            return Course(record[0], record[1], record[2], record[3], record[4])
        return None

    def save(self):
        # Lưu hoặc cập nhật bản ghi môn học
        if find_record(self.FILE, 0, self._courseCode):
            return update_record(self.FILE, 0, self._courseCode, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    def delete(self):
        return delete_record(self.FILE, 0, self._courseCode)

    @staticmethod
    def find_by_code(code):
        # Tìm môn học theo mã
        record = find_record(Course.FILE, 0, code)
        return Course.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả môn học
        return [Course.from_record(r) for r in read_records(Course.FILE)
                if Course.from_record(r) is not None]

    @staticmethod
    def find_by_faculty(faculty_code):
        # Tìm tất cả môn học thuộc một khoa
        from utils.file_handler import find_all_records
        records = find_all_records(Course.FILE, 3, faculty_code)
        return [Course.from_record(r) for r in records if Course.from_record(r) is not None]
