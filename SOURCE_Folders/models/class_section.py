# models/class_section.py  –  Lớp học phần

from utils.file_handler import read_file, write_file

class ClassSection:
    def __init__(self, class_code, course_code, semester_id, max_capacity, current_enrollment=0,
                 day_of_week="", start_time="", end_time="", room="", employee_id=""):
        # Khai báo các public attributes
        self.class_code         = class_code          # PK - Mã lớp (VD: IT001.01)
        self.course_code        = course_code         # FK - Tham chiếu Môn học
        self.semester_id        = semester_id         # FK - Tham chiếu Học kỳ
        self.employee_id        = employee_id         # FK - Tham chiếu Giảng viên (Rỗng = chưa phân công)
        self.max_capacity       = int(max_capacity)   # Sĩ số tối đa
        self.current_enrollment = int(current_enrollment) # Số SV hiện tại đã đăng ký
        self.day_of_week        = day_of_week         # Thứ học trong tuần
        self.start_time         = start_time          # Giờ bắt đầu
        self.end_time           = end_time            # Giờ kết thúc
        self.room               = room                # Phòng học

    #CÁC HÀM CRUD (Tương tác với File qua file_handler)
    #Lấy toàn bộ danh sách Lớp học phần từ file .txt
    @classmethod
    def get_all(cls):
        records = read_file("data/class_sections.txt")
        return [cls(
            class_code=r["class_code"],
            course_code=r["course_code"],
            semester_id=r["semester_id"],
            employee_id=r.get("employee_id", ""),
            max_capacity=r.get("max_capacity", 0),
            current_enrollment=r.get("current_enrollment", 0),
            day_of_week=r.get("day_of_week", ""),
            start_time=r.get("start_time", ""),
            end_time=r.get("end_time", ""),
            room=r.get("room", "")
        ) for r in records]

    #Tìm một Lớp học phần cụ thể theo Mã lớp.
    @classmethod
    def find_by_id(cls, class_code):
        for s in cls.get_all():
            if s.class_code.upper() == class_code.upper():
                return s
        return None

    #Lấy tất cả các lớp của 1 môn học.
    @classmethod
    def find_by_course(cls, course_code):
        return [s for s in cls.get_all() if s.course_code.upper() == course_code.upper()]

    #Lấy tất cả các lớp đang mở trong 1 học kỳ.
    @classmethod
    def find_by_semester(cls, semester_id):
        return [s for s in cls.get_all() if s.semester_id.upper() == semester_id.upper()]
    
    #Trả list các lớp mà một giảng viên được phân công giảng dạy.
    @classmethod
    def find_by_lecturer(cls, employee_id):
        return [s for s in cls.get_all() if s.employee_id == employee_id]

    #Lưu lớp học phần vào file (Thêm mới hoặc Cập nhật).
    def save(self):
        records = read_file("data/class_sections.txt")
        
        # Gom dữ liệu hiện tại vào Dictionary
        new_record = {
            "class_code": self.class_code,
            "course_code": self.course_code,
            "semester_id": self.semester_id,
            "employee_id": self.employee_id,
            "max_capacity": str(self.max_capacity),
            "current_enrollment": str(self.current_enrollment),
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "room": self.room
        }
        
        updated = False
        for i, r in enumerate(records):
            if r.get("class_code") == self.class_code:
                records[i] = new_record
                updated = True
                break
                
        if not updated:
            records.append(new_record)
            
        write_file("data/class_sections.txt", records)
        return True

    #Xóa lớp học phần khỏi hệ thống
    @classmethod
    def delete(cls, class_code):
        records = read_file("data/class_sections.txt")
        records = [r for r in records if r.get("class_code") != class_code]
        write_file("data/class_sections.txt", records)
        return True

    #LOGIC NGHIỆP VỤ (Business Logic)

    #Kiểm tra xem lớp đã đầy sinh viên chưa
    def is_full(self):
        return self.current_enrollment >= self.max_capacity

    #True nếu mã lớp đã tồn tại trước đó
    def is_duplicate(self):
        return self.find_by_id(self.class_code) is not None

    #Phân công giảng viên cho lớp học này.
    def assign_lecturer(self, employee_id):
        self.employee_id = employee_id

    #Cập nhật số lượng SV đăng ký. 1. Truyền delta = 1 khi có SV đăng ký mới, delta = -1 khi SV hủy môn. 2. Trả về True nếu hợp lệ, False nếu lớp đã đầy hoặc số lượng bị âm.
    def update_enrollment(self, delta):
        new_count = self.current_enrollment + delta
        if new_count < 0 or new_count > self.max_capacity:
            return False
            
        self.current_enrollment = new_count
        return True

    def __str__(self):
        return (f"[{self.class_code}] Môn: {self.course_code} "
                f"| HK: {self.semester_id} "
                f"| Thứ {self.day_of_week} {self.start_time}-{self.end_time} "
                f"| Phòng: {self.room} "
                f"| SL: {self.current_enrollment}/{self.max_capacity} "
                f"| GV: {self.employee_id or 'Chưa phân công'}")