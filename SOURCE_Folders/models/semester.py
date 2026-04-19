# models/semester.py  –  Quản lý học kỳ

from utils.file_handler import read_file, write_file

class Semester:
    def __init__(self, semester_id, semester_name, start_date, end_date, exam_week_start="", exam_week_end=""):
        self.__semester_id = semester_id              # PK - Khóa chính (Mã học kỳ)
        self.__semester_name = semester_name          # Tên học kỳ
        self.__start_date = start_date                # Ngày bắt đầu
        self.__end_date = end_date                    # Ngày kết thúc
        self.__exam_week_start = exam_week_start      # Ngày bắt đầu tuần thi
        self.__exam_week_end = exam_week_end          # Ngày kết thúc tuần thi

    #GETTERS / SETTERS

    @property
    def semester_id(self):
        return self.__semester_id

    @property
    def semester_name(self):
        return self.__semester_name
    
    @semester_name.setter
    def semester_name(self, value):
        self.__semester_name = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        self.__end_date = value

    @property
    def exam_week_start(self):
        return self.__exam_week_start

    @exam_week_start.setter
    def exam_week_start(self, value):
        self.__exam_week_start = value

    @property
    def exam_week_end(self):
        return self.__exam_week_end

    @exam_week_end.setter
    def exam_week_end(self, value):
        self.__exam_week_end = value

    #CLASS METHODS (Các thao tác CRUD tương tác với File)

    # Hàm tìm kiếm 1 Học kỳ cụ thể theo Mã học kỳ (semester_id)
    @classmethod
    def find_by_id(cls, semester_id):
        records = read_file("data/semesters.txt") # Đọc file lấy danh sách Dictionary
        for record in records:
            # Nếu tìm thấy dictionary có ID khớp
            if record.get("semester_id") == semester_id:
                # Chuyển dictionary đó thành đối tượng Semester và trả về
                return cls(
                    semester_id=record["semester_id"],
                    semester_name=record["semester_name"],
                    start_date=record["start_date"],
                    end_date=record["end_date"],
                    exam_week_start=record.get("exam_week_start", ""),
                    exam_week_end=record.get("exam_week_end", "")
                )
        return None # Trả về None nếu duyệt hết mà không tìm thấy

    # Hàm lấy toàn bộ danh sách Học kỳ hiện có
    @classmethod
    def get_all(cls):
        records = read_file("data/semesters.txt")
        semesters = []
        for record in records:
            # Duyệt qua từng Dictionary, biến nó thành đối tượng Semester rồi nhét vào mảng semesters
            semesters.append(cls(
                semester_id=record["semester_id"],
                semester_name=record["semester_name"],
                start_date=record["start_date"],
                end_date=record["end_date"],
                exam_week_start=record.get("exam_week_start", ""),
                exam_week_end=record.get("exam_week_end", "")
            ))
        return semesters

    # Hàm Lưu học kỳ vào file (Bao gồm cả Thêm mới và Cập nhật)
    def save(self):
        records = read_file("data/semesters.txt")
        
        # Đóng gói thông tin hiện tại của đối tượng này thành 1 Dictionary mới
        new_record = {
            "semester_id": self.__semester_id,
            "semester_name": self.__semester_name,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "exam_week_start": self.__exam_week_start,
            "exam_week_end": self.__exam_week_end
        }
        
        updated = False
        # Duyệt danh sách cũ, nếu tìm thấy ID đã tồn tại thì tiến hành ghi đè (Update)
        for i, record in enumerate(records):
            if record.get("semester_id") == self.__semester_id:
                records[i] = new_record
                updated = True
                break
                
        # Nếu duyệt hết mà chưa Update (nghĩa là ID này mới toanh) -> Thêm vào cuối danh sách (Insert)
        if not updated:
            records.append(new_record)
            
        write_file("data/semesters.txt", records) # Ghi mảng đã chỉnh sửa đè lại vào file text
        return True

    # Hàm xóa Học kỳ theo ID
    @classmethod
    def delete(cls, semester_id):
        records = read_file("data/semesters.txt")
        # Dùng List Comprehension để giữ lại tất cả các record KHÁC với ID cần xóa (bản chất là Lọc/Xóa)
        records = [r for r in records if r.get("semester_id") != semester_id]
        write_file("data/semesters.txt", records)
        return True

    #VALIDATION (Logic kiểm tra tính hợp lệ dữ liệu)

    def is_valid(self):
        if not self.__semester_id.strip():
            return False, "Mã học kỳ không được để trống"
        if not self.__semester_name.strip():
            return False, "Tên học kỳ không được để trống"
        if not self.__start_date.strip():
            return False, "Ngày bắt đầu không được để trống"
        if not self.__end_date.strip():
            return False, "Ngày kết thúc không được để trống"
        return True, ""

    def is_duplicate(self):
        return self.find_by_id(self.__semester_id) is not None