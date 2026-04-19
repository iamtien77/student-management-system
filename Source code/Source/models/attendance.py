# Lớp Attendance (Điểm danh) - Ánh xạ tới D8 (Kho dữ liệu Điểm danh)
# Thuộc tính: sessionDate, attendanceStatus, absenceCount (tính toán), attendanceRate (tính toán)
# Phương thức: markAttendance, calculateAttendanceRate

from utils.file_handler import (read_records, find_all_records, append_line, write_records)


class Attendance:
    # Tên file lưu trữ dữ liệu điểm danh
    FILE = "attendance.txt"

    def __init__(self, classCode, studentID, sessionDate, attendanceStatus="Present"):
        self._classCode = classCode               # Mã lớp học phần (FK tới ClassSection)
        self._studentID = studentID               # Mã sinh viên (FK tới Student)
        self._sessionDate = sessionDate           # Ngày buổi học (DD/MM/YYYY)
        self._attendanceStatus = attendanceStatus # Trạng thái: Present (có mặt) / Absent (vắng)

    # Thuộc tính

    @property
    def classCode(self):
        return self._classCode

    @property
    def studentID(self):
        return self._studentID

    @property
    def sessionDate(self):
        return self._sessionDate

    @property
    def attendanceStatus(self):
        return self._attendanceStatus

    @property
    def absenceCount(self):
        # Thuộc tính tính toán: đếm số buổi vắng của SV trong lớp này
        records = self.get_student_class_records(self._studentID, self._classCode)
        return sum(1 for r in records if r.attendanceStatus == "Absent")

    @property
    def attendanceRate(self):
        # Thuộc tính tính toán: tỷ lệ đi học của SV trong lớp này
        return self.calculateAttendanceRate()

    # Phương thức theo Class Diagram

    def markAttendance(self, status):
        # UC16: Đánh dấu trạng thái điểm danh cho sinh viên
        # Nếu đã có bản ghi cho ngày này thì cập nhật, chưa có thì thêm mới
        self._attendanceStatus = status
        records = read_records(self.FILE)
        for i, r in enumerate(records):
            if (len(r) >= 4 and r[0] == self._classCode and
                    r[1] == self._studentID and r[2] == self._sessionDate):
                # Cập nhật bản ghi đã tồn tại
                records[i] = self.to_record()
                return write_records(self.FILE, records)
        # Thêm bản ghi mới
        return append_line(self.FILE, "|".join(self.to_record()))

    def calculateAttendanceRate(self):
        # Tính tỷ lệ đi học = số buổi có mặt / tổng số buổi × 100%
        records = self.get_student_class_records(self._studentID, self._classCode)
        if not records:
            return 0.0
        total = len(records)
        present = sum(1 for r in records if r.attendanceStatus == "Present")
        return round(present / total * 100, 1)

    # Chuyển đổi dữ liệu

    def to_record(self):
        return [self._classCode, self._studentID,
                self._sessionDate, self._attendanceStatus]

    @staticmethod
    def from_record(record):
        if len(record) >= 4:
            return Attendance(*record[:4])
        return None

    # Các hàm truy vấn hỗ trợ

    @staticmethod
    def get_student_class_records(student_id, class_code):
        # Lấy tất cả bản ghi điểm danh của 1 SV trong 1 lớp
        results = []
        for r in read_records(Attendance.FILE):
            if len(r) >= 4 and r[0] == class_code and r[1] == student_id:
                att = Attendance.from_record(r)
                if att:
                    results.append(att)
        return results

    @staticmethod
    def get_class_session(class_code, session_date):
        # Lấy tất cả bản ghi điểm danh của 1 lớp trong 1 ngày cụ thể
        results = []
        for r in read_records(Attendance.FILE):
            if len(r) >= 4 and r[0] == class_code and r[2] == session_date:
                att = Attendance.from_record(r)
                if att:
                    results.append(att)
        return results

    @staticmethod
    def get_class_records(class_code):
        # Lấy tất cả bản ghi điểm danh của 1 lớp
        records = find_all_records(Attendance.FILE, 0, class_code)
        return [Attendance.from_record(r) for r in records
                if Attendance.from_record(r) is not None]

    @staticmethod
    def get_sessions_for_class(class_code):
        # Lấy danh sách các ngày đã điểm danh của 1 lớp (không trùng lặp)
        records = find_all_records(Attendance.FILE, 0, class_code)
        dates = set()
        for r in records:
            if len(r) >= 3:
                dates.add(r[2])
        return sorted(list(dates))
