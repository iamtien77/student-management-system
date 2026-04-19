# Lớp ClassSection (Lớp học phần) - Ánh xạ tới D6 (Kho dữ liệu Lớp học phần)
# Thuộc tính: classCode, maxCapacity, currentEnrollment, dayOfWeek, startTime, endTime, room
# Quan hệ: thuộc về Course (1), Semester (1), Lecturer dạy (1)

from utils.file_handler import (read_records, find_record, find_all_records,
                                 update_record, append_line, delete_record)


class ClassSection:
    # Tên file lưu trữ dữ liệu lớp học phần
    FILE = "classes.txt"

    def __init__(self, classCode, courseCode="", semesterCode="",
                 maxCapacity=0, currentEnrollment=0, dayOfWeek="",
                 startTime="", endTime="", room="", lecturerID=""):
        self._classCode = classCode               # Mã lớp học phần
        self._courseCode = courseCode              # Mã môn học (FK tới Course)
        self._semesterCode = semesterCode         # Mã học kỳ (FK tới Semester)
        self._maxCapacity = int(maxCapacity) if maxCapacity else 0      # Sĩ số tối đa
        self._currentEnrollment = int(currentEnrollment) if currentEnrollment else 0  # Số SV hiện tại
        self._dayOfWeek = dayOfWeek               # Thứ trong tuần
        self._startTime = startTime               # Giờ bắt đầu
        self._endTime = endTime                   # Giờ kết thúc
        self._room = room                         # Phòng học
        self._lecturerID = lecturerID             # Mã giảng viên phụ trách (FK tới Lecturer)

    # Thuộc tính

    @property
    def classCode(self):
        return self._classCode

    @property
    def courseCode(self):
        return self._courseCode

    @property
    def semesterCode(self):
        return self._semesterCode

    @property
    def maxCapacity(self):
        return self._maxCapacity

    @property
    def currentEnrollment(self):
        return self._currentEnrollment

    @property
    def dayOfWeek(self):
        return self._dayOfWeek

    @property
    def startTime(self):
        return self._startTime

    @property
    def endTime(self):
        return self._endTime

    @property
    def room(self):
        return self._room

    @property
    def lecturerID(self):
        return self._lecturerID

    # Phương thức theo Class Diagram

    def isFull(self):
        # Kiểm tra lớp đã đầy chưa
        return self._currentEnrollment >= self._maxCapacity

    def hasScheduleConflict(self, other):
        # Kiểm tra xung đột lịch với lớp khác
        # Nếu khác thứ thì không xung đột
        if self._dayOfWeek != other._dayOfWeek:
            return False
        # So sánh khoảng thời gian
        try:
            s1 = self._startTime.replace(":", "")
            e1 = self._endTime.replace(":", "")
            s2 = other._startTime.replace(":", "")
            e2 = other._endTime.replace(":", "")
            # Xung đột khi hai khoảng thời gian giao nhau
            return not (e1 <= s2 or e2 <= s1)
        except Exception:
            return False

    # Chuyển đổi dữ liệu

    def to_record(self):
        return [self._classCode, self._courseCode, self._semesterCode,
                str(self._maxCapacity), str(self._currentEnrollment),
                self._dayOfWeek, self._startTime, self._endTime,
                self._room, self._lecturerID]

    @staticmethod
    def from_record(record):
        if len(record) >= 10:
            return ClassSection(*record[:10])
        return None

    def save(self):
        # Lưu hoặc cập nhật bản ghi lớp học phần
        if find_record(self.FILE, 0, self._classCode):
            return update_record(self.FILE, 0, self._classCode, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    def delete(self):
        return delete_record(self.FILE, 0, self._classCode)

    @staticmethod
    def find_by_code(code):
        # Tìm lớp học phần theo mã
        record = find_record(ClassSection.FILE, 0, code)
        return ClassSection.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả lớp học phần
        return [ClassSection.from_record(r) for r in read_records(ClassSection.FILE)
                if ClassSection.from_record(r) is not None]

    @staticmethod
    def find_by_lecturer(lecturer_id):
        # Tìm tất cả lớp do một giảng viên phụ trách
        records = find_all_records(ClassSection.FILE, 9, lecturer_id)
        return [ClassSection.from_record(r) for r in records
                if ClassSection.from_record(r) is not None]

    @staticmethod
    def find_by_semester(semester_code):
        # Tìm tất cả lớp trong một học kỳ
        records = find_all_records(ClassSection.FILE, 2, semester_code)
        return [ClassSection.from_record(r) for r in records
                if ClassSection.from_record(r) is not None]
