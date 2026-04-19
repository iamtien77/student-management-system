# Lớp TrainingProgram (Chương trình đào tạo) - Ánh xạ tới D5 (Kho dữ liệu CTĐT)
# Thuộc tính: programID, programName, courses (List<Course>)
# Phương thức: getCourseStatus(course) - trả về Completed/Incomplete

from utils.file_handler import read_records, find_record, update_record, append_line, delete_record


class TrainingProgram:
    # Tên file lưu trữ chương trình đào tạo
    FILE = "curriculum.txt"

    def __init__(self, programID, programName="", courseCodes=""):
        self._programID = programID         # Mã chương trình đào tạo
        self._programName = programName     # Tên chương trình
        # Danh sách mã môn học lưu dạng chuỗi phân cách bởi dấu phẩy
        self._courseCodes = courseCodes

    @property
    def programID(self):
        return self._programID

    @property
    def programName(self):
        return self._programName

    @property
    def courseCodes(self):
        return self._courseCodes

    def get_course_list(self):
        # Trả về danh sách đối tượng Course trong chương trình này
        from models.course import Course
        if not self._courseCodes or self._courseCodes.strip() == "":
            return []
        codes = [c.strip() for c in self._courseCodes.split(",") if c.strip()]
        courses = []
        for code in codes:
            c = Course.find_by_code(code)
            if c:
                courses.append(c)
        return courses

    def getCourseStatus(self, courseCode, studentID):
        # UC15: Xác định trạng thái môn học là Completed hay Incomplete
        # Dựa trên bảng điểm của sinh viên
        from models.grade import Grade
        grades = Grade.find_by_student(studentID)
        for g in grades:
            if g.status == "Finalized":
                from models.class_section import ClassSection
                cs = ClassSection.find_by_code(g.classCode)
                # Hoàn thành nếu: điểm đã duyệt + đúng môn + không rớt (khác F)
                if cs and cs.courseCode == courseCode and g.letterGrade != "F":
                    return "Completed"
        return "Incomplete"

    def to_record(self):
        return [self._programID, self._programName, self._courseCodes]

    @staticmethod
    def from_record(record):
        if len(record) >= 3:
            return TrainingProgram(record[0], record[1], record[2])
        return None

    def save(self):
        # Lưu hoặc cập nhật chương trình đào tạo
        if find_record(self.FILE, 0, self._programID):
            return update_record(self.FILE, 0, self._programID, self.to_record())
        return append_line(self.FILE, "|".join(self.to_record()))

    @staticmethod
    def find_by_id(program_id):
        # Tìm chương trình đào tạo theo mã
        record = find_record(TrainingProgram.FILE, 0, program_id)
        return TrainingProgram.from_record(record) if record else None

    @staticmethod
    def get_all():
        # Lấy danh sách tất cả chương trình đào tạo
        return [TrainingProgram.from_record(r) for r in read_records(TrainingProgram.FILE)
                if TrainingProgram.from_record(r) is not None]
