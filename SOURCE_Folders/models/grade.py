# models/grade.py  –  Điểm số và kết quả học tập

from utils.file_handler import read_file, write_file

STATUS_DRAFT     = "draft"      # Điểm nháp, giảng viên có thể sửa
STATUS_FINALIZED = "finalized"  # Điểm đã chốt, không thể sửa

class Grade:
    def __init__(self, grade_id, student_id, class_code, midterm_grade=0.0, assignment_grade=0.0,
                 attendance_grade=0.0, final_exam_grade=0.0, final_summary_grade=0.0, letter_grade="", status=STATUS_DRAFT):
        # Khai báo các biến (thuộc tính) public, bên ngoài có thể truy cập và gán giá trị trực tiếp
        self.grade_id = grade_id
        self.student_id = student_id
        self.class_code = class_code
        self.midterm_grade = float(midterm_grade)
        self.assignment_grade = float(assignment_grade)
        self.attendance_grade = float(attendance_grade)
        self.final_exam_grade = float(final_exam_grade)
        self.final_summary_grade = float(final_summary_grade)
        self.letter_grade = letter_grade
        self.status = status

    #CÁC HÀM CRUD (Thao tác với Dữ liệu qua file text)
    # Hàm lấy toàn bộ danh sách điểm từ file
    @classmethod
    def get_all(cls):
        records = read_file("data/grades.txt") # Đọc file, trả về list các Dictionary
        # Chuyển đổi từng Dictionary thành đối tượng Grade và đưa vào một list (List Comprehension)
        return [cls(
            grade_id=r["grade_id"],
            student_id=r["student_id"],
            class_code=r["class_code"],
            midterm_grade=r.get("midterm_grade", 0),
            assignment_grade=r.get("assignment_grade", 0),
            attendance_grade=r.get("attendance_grade", 0),
            final_exam_grade=r.get("final_exam_grade", 0),
            final_summary_grade=r.get("final_summary_grade", 0),
            letter_grade=r.get("letter_grade", ""),
            status=r.get("status", STATUS_DRAFT)
        ) for r in records]

    # Hàm tìm kiếm 1 cột điểm cụ thể dựa vào mã điểm (grade_id)
    @classmethod
    def find_by_id(cls, grade_id):
        for g in cls.get_all():
            if g.grade_id == grade_id:
                return g
        return None

    # Hàm tìm điểm của 1 sinh viên cụ thể trong 1 lớp học phần cụ thể
    @classmethod
    def find_by_student_and_class(cls, student_id, class_code):
        for g in cls.get_all():
            if g.student_id == student_id and g.class_code.upper() == class_code.upper():
                return g
        return None

    # Hàm lấy toàn bộ bảng điểm của 1 sinh viên
    # Tham số finalized_only=True nghĩa là chỉ lấy những điểm đã chốt (để tính GPA hoặc in bảng điểm chính thức)
    @classmethod
    def find_by_student(cls, student_id, finalized_only=False):
        result = []
        for g in cls.get_all():
            if g.student_id != student_id:
                continue # Nếu không phải sinh viên này thì bỏ qua
            if finalized_only and g.status != STATUS_FINALIZED:
                continue # Nếu yêu cầu chỉ lấy điểm chốt mà điểm này đang là nháp thì bỏ qua
            result.append(g)
        return result

    # Hàm lấy toàn bộ danh sách điểm của 1 lớp học phần (Dành cho Giảng viên xem điểm lớp mình dạy)
    @classmethod
    def find_by_class(cls, class_code):
        return [g for g in cls.get_all() if g.class_code.upper() == class_code.upper()]

    # Hàm Lưu điểm (Thêm mới hoặc Cập nhật)
    def save(self):
        """Lưu điểm vào file (Update hoặc Insert)."""
        existing = self.find_by_id(self.grade_id)
        # Ràng buộc hệ thống: Trả về lỗi nếu điểm đã bị khóa (finalized)
        if existing and existing.status == STATUS_FINALIZED:
            return False, "Điểm đã được chốt, không thể chỉnh sửa"
        
        records = read_file("data/grades.txt")
        # Gom các thông tin hiện tại thành một Dictionary để chuẩn bị ghi vào file
        new_record = {
            "grade_id": self.grade_id,
            "student_id": self.student_id,
            "class_code": self.class_code,
            "midterm_grade": str(self.midterm_grade),
            "assignment_grade": str(self.assignment_grade),
            "attendance_grade": str(self.attendance_grade),
            "final_exam_grade": str(self.final_exam_grade),
            "final_summary_grade": str(self.final_summary_grade),
            "letter_grade": self.letter_grade,
            "status": self.status
        }
        
        updated = False
        # Tìm xem đã có bản ghi nào trùng grade_id chưa, nếu có thì ghi đè (Cập nhật)
        for i, r in enumerate(records):
            if r.get("grade_id") == self.grade_id:
                records[i] = new_record
                updated = True
                break
        
        # Nếu duyệt hết mà chưa có (updated = False), nghĩa là điểm mới -> Thêm vào danh sách (Insert)
        if not updated:
            records.append(new_record)
            
        write_file("data/grades.txt", records) # Ghi ngược lại toàn bộ list vào file txt
        return True, ""

    # Hàm Chốt điểm toàn bộ lớp học phần (Chỉ Admin được gọi)
    @classmethod
    def finalize_by_class(cls, class_code):
        grades = cls.get_all()
        count = 0
        for g in grades:
            # Tìm các điểm thuộc lớp này và đang ở trạng thái nháp (draft)
            if g.class_code.upper() == class_code.upper() and g.status == STATUS_DRAFT:
                g.status = STATUS_FINALIZED # Chuyển thành chốt
                g.save() # Gọi hàm save() để lưu bản ghi này lại
                count += 1
        return True, count # Trả về báo thành công và số lượng điểm đã chốt

    # Hàm tự động sinh mã Điểm mới (vd: GR001, GR002) cho dữ liệu không bị trùng
    @classmethod
    def generate_id(cls):
        all_g = cls.get_all()
        if not all_g:
            return "GR001"
        last = all_g[-1].grade_id # Lấy ID của phần tử cuối cùng
        try:
            num = int(last.replace("GR", "")) # Cắt chữ "GR" lấy số, ép kiểu int
            return f"GR{num + 1:03d}"         # Cộng 1 rồi format lại thành 3 chữ số (001, 002)
        except ValueError:
            return f"GR{len(all_g) + 1:03d}"

    #LOGIC NGHIỆP VỤ (Các tính toán đặc thù của hệ thống)

    # Tính điểm tổng kết dựa trên công thức trọng số %
    def calculate_summary_grade(self):
        """Tính finalSummaryGrade và letterGrade."""
        self.final_summary_grade = round(
            self.attendance_grade * 0.10 +   # Chuyên cần 10%
            self.assignment_grade * 0.20 +   # Bài tập 20%
            self.midterm_grade    * 0.20 +   # Giữa kỳ 20%
            self.final_exam_grade * 0.50,    # Cuối kỳ 50%
            2                                # Làm tròn 2 chữ số thập phân
        )
        # Gọi hàm chuyển đổi để xếp loại A, B, C...
        self.letter_grade = self._to_letter(self.final_summary_grade)

    # Hàm tĩnh: Chuyển từ điểm số sang điểm chữ
    @staticmethod
    def _to_letter(score):
        if score >= 8.5: return "A"
        elif score >= 7.0: return "B"
        elif score >= 5.5: return "C"
        elif score >= 4.0: return "D"
        return "F"

    # Hàm tĩnh: Chuyển từ điểm chữ sang thang điểm 4.0 để tính GPA
    @staticmethod
    def _letter_to_point(letter):
        return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}.get(letter.upper(), 0.0)

    # Hàm tính điểm trung bình học kỳ (GPA)
    @classmethod
    def calculate_semester_gpa(cls, student_id, class_credits_map):
        # Lấy danh sách điểm đã chốt của sinh viên
        grades = cls.find_by_student(student_id, finalized_only=True)
        total_points = 0.0
        total_credits = 0
        for g in grades:
            # class_credits_map là mảng 1 chiều chứa [Mã Lớp : Số tín chỉ]. Nếu lớp không nằm trong kỳ này thì bỏ qua
            if g.class_code not in class_credits_map:
                continue
            credits = class_credits_map[g.class_code]
            # Công thức GPA: (Điểm hệ 4 x Số tín chỉ) / Tổng số tín chỉ
            total_points += cls._letter_to_point(g.letter_grade) * credits
            total_credits += credits
        
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 2)

    # Hàm tính điểm trung bình tích lũy (Cơ chế tính giống GPA học kỳ nhưng map tín chỉ truyền vào sẽ là tất cả các kỳ)
    @classmethod
    def calculate_cumulative_gpa(cls, student_id, all_class_credits_map):
        return cls.calculate_semester_gpa(student_id, all_class_credits_map)

    # Lọc ra danh sách mã Môn học (Courses) mà sinh viên đã thi Đậu (Khác điểm F)
    @classmethod
    def get_completed_courses(cls, student_id):
        grades = cls.find_by_student(student_id, finalized_only=True)
        done = []
        for g in grades:
            if g.letter_grade and g.letter_grade.upper() != "F":
                # Giả định: class_code có dạng "IT001.1", tách dấu chấm lấy phần đầu ("IT001") là mã Môn học
                course_code = g.class_code.split(".")[0] 
                if course_code not in done:
                    done.append(course_code)
        return done