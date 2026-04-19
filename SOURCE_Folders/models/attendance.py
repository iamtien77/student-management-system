# models/attendance.py  –  Điểm danh sinh viên

from utils.file_handler import read_file, write_file

# Khai báo các hằng số trạng thái hợp lệ
STATUS_PRESENT = "present"
STATUS_ABSENT  = "absent"
STATUS_LATE    = "late"
VALID_STATUSES = {STATUS_PRESENT, STATUS_ABSENT, STATUS_LATE}

class Attendance:
    def __init__(self, attendance_id, student_id, class_code, session_date, status=STATUS_PRESENT):
        # Khai báo public attributes, Views/Controllers có thể đọc/ghi trực tiếp
        self.attendance_id = attendance_id
        self.student_id    = student_id    # FK → Student
        self.class_code    = class_code    # FK → ClassSection
        self.session_date  = session_date
        # Validate status – nếu truyền vào chữ tào lao không hợp lệ thì tự mặc định là present
        self.status = status if status in VALID_STATUSES else STATUS_PRESENT

    #CÁC HÀM CRUD (Tương tác với File qua file_handler)
    #Lấy toàn bộ danh sách điểm danh từ file .txt
    @classmethod
    def get_all(cls):
        records = read_file("data/attendance.txt")
        return [cls(
            attendance_id=r["attendance_id"],
            student_id=r["student_id"],
            class_code=r["class_code"],
            session_date=r["session_date"],
            status=r.get("status", STATUS_PRESENT)
        ) for r in records]
    
    #Tìm 1 bản ghi điểm danh cụ thể theo ID.
    @classmethod
    def find_by_id(cls, attendance_id):
        for r in cls.get_all():
            if r.attendance_id == attendance_id:
                return r
        return None
    
    #Trả list tất cả các buổi điểm danh của 1 Sinh viên cụ thể trong 1 Lớp cụ thể.
    @classmethod
    def find_by_student_and_class(cls, student_id, class_code):
        return [r for r in cls.get_all()
                if r.student_id == student_id and r.class_code.upper() == class_code.upper()]

    #Lấy danh sách điểm danh của toàn bộ SV trong 1 Lớp vào 1 Ngày cụ thể.
    @classmethod
    def find_by_class_and_date(cls, class_code, session_date):
        return [r for r in cls.get_all()
                if r.class_code.upper() == class_code.upper() and r.session_date == session_date]

    #Trả toàn bộ dữ liệu điểm danh của 1 Lớp
    @classmethod
    def find_by_class(cls, class_code):
        return [r for r in cls.get_all()
                if r.class_code.upper() == class_code.upper()]

    #Lưu điểm danh vào file (Update hoặc Insert).
    def save(self):
        records = read_file("data/attendance.txt")
        
        # Gom các thông tin hiện tại thành một Dictionary để ghi vào file
        new_record = {
            "attendance_id": self.attendance_id,
            "student_id": self.student_id,
            "class_code": self.class_code,
            "session_date": self.session_date,
            "status": self.status
        }
        
        updated = False
        for i, r in enumerate(records):
            # Nếu tìm thấy ID trùng -> Cập nhật trạng thái điểm danh
            if r.get("attendance_id") == self.attendance_id:
                records[i] = new_record
                updated = True
                break
                
        # Nếu duyệt hết mà chưa có ID này -> Thêm buổi điểm danh mới
        if not updated:
            records.append(new_record)
            
        write_file("data/attendance.txt", records)
        return True

    #LOGIC NGHIỆP VỤ (Business Logic)

    #Tính tỷ lệ điểm danh (%) của 1 SV trong 1 lớp; (số buổi có mặt + đi trễ) / tổng số buổi * 100. Trả 100.0 nếu chưa có buổi nào diễn ra.
    @classmethod
    def calculate_attendance_rate(cls, student_id, class_code):
        records = cls.find_by_student_and_class(student_id, class_code)
        if not records:
            return 100.0
            
        # Đếm số buổi vắng
        absent_count = sum(1 for r in records if r.status == STATUS_ABSENT)
        present_count = len(records) - absent_count
        
        return round(present_count / len(records) * 100, 1)

    #Đếm số buổi vắng mặt của 1 SV trong 1 lớp.
    @classmethod
    def get_absence_count(cls, student_id, class_code):
        records = cls.find_by_student_and_class(student_id, class_code)
        return sum(1 for r in records if r.status == STATUS_ABSENT)

    #  Tự tạo mã điểm danh tăng dần: ATT001, ATT002, ..  Tránh việc trùng lặp Khóa chính (PK).
    @classmethod
    def generate_id(cls):
        all_r = cls.get_all()
        if not all_r:
            return "ATT001"
        last = all_r[-1].attendance_id
        try:
            num = int(last.replace("ATT", ""))
            return f"ATT{num + 1:03d}"
        except ValueError:
            return f"ATT{len(all_r) + 1:03d}"

    def __str__(self):
        return (f"[{self.attendance_id}] SV: {self.student_id} "
                f"| Lớp: {self.class_code} "
                f"| Ngày: {self.session_date} "
                f"| Trạng thái: {self.status}")