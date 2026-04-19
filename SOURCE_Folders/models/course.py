# models/course.py  –  Danh mục môn học
# Tách thành 2 file dữ liệu khớp với data model:
#   data/courses.txt              → thông tin môn học (course_code, course_name, credits, faculty_code)
#   data/course_prerequisites.txt → junction table CoursePrerequisite (course_code, prerequisite_code)

from utils.file_handler import read_file, write_file


class Course:

    def __init__(self, course_code, course_name, credits, faculty_code):
        self.course_code  = course_code
        self.course_name  = course_name
        self.credits      = int(credits)
        self.faculty_code = faculty_code
        # Không lưu prerequisites trực tiếp trong object nữa.
        # Dùng CoursePrerequisite.get_prerequisites_of(course_code) khi cần.

    # -------------------------------------------------------------------------
    # CÁC HÀM CRUD – Course (tương tác với courses.txt)
    # -------------------------------------------------------------------------

    # Trả list tất cả Course
    @classmethod
    def get_all(cls):
        records = read_file("data/courses.txt")
        return [cls(
            course_code=r["course_code"],
            course_name=r["course_name"],
            credits=r["credits"],
            faculty_code=r["faculty_code"]
        ) for r in records]

    # Tìm theo mã môn, trả None nếu không có
    @classmethod
    def find_by_id(cls, course_code):
        for c in cls.get_all():
            if c.course_code.upper() == course_code.upper():
                return c
        return None

    # Trả list môn học thuộc một khoa
    @classmethod
    def find_by_faculty(cls, faculty_code):
        return [c for c in cls.get_all()
                if c.faculty_code.upper() == faculty_code.upper()]

    # Thêm mới hoặc cập nhật, trả True/False
    def save(self):
        records = read_file("data/courses.txt")
        new_record = {
            "course_code":  self.course_code,
            "course_name":  self.course_name,
            "credits":      str(self.credits),
            "faculty_code": self.faculty_code
        }

        updated = False
        for i, r in enumerate(records):
            if r.get("course_code", "").upper() == self.course_code.upper():
                records[i] = new_record
                updated = True
                break

        if not updated:
            records.append(new_record)

        write_file("data/courses.txt", records)
        return True

    # Xoá theo mã môn; đồng thời xoá luôn prerequisites liên quan
    @classmethod
    def delete(cls, course_code):
        records = read_file("data/courses.txt")
        new_records = [r for r in records
                       if r.get("course_code", "").upper() != course_code.upper()]

        if len(new_records) == len(records):
            return False  # Không tìm thấy để xoá

        write_file("data/courses.txt", new_records)

        # Dọn sạch junction table: xoá các dòng có course_code hoặc prerequisite_code trùng
        CoursePrerequisite.delete_by_course(course_code)
        return True

    # -------------------------------------------------------------------------
    # LOGIC NGHIỆP VỤ
    # -------------------------------------------------------------------------

    # True nếu mã môn đã tồn tại (dùng khi thêm mới để tránh trùng PK)
    def is_duplicate(self):
        return self.find_by_id(self.course_code) is not None

    # Lấy danh sách mã môn tiên quyết của môn này (query sang junction table)
    def get_prerequisites(self):
        return CoursePrerequisite.get_prerequisites_of(self.course_code)

    def __str__(self):
        prereqs = CoursePrerequisite.get_prerequisites_of(self.course_code)
        pre_str = ", ".join(prereqs) if prereqs else "Không có"
        return (f"[{self.course_code}] {self.course_name} "
                f"| {self.credits} TC | Khoa: {self.faculty_code} "
                f"| Tiên quyết: {pre_str}")


# =============================================================================
# Junction table: CoursePrerequisite  (course_code  <-->  prerequisite_code)
# Tương đương bảng CoursePrerequisite trong data model / drawio diagram
# File lưu trữ: data/course_prerequisites.txt
# =============================================================================

class CoursePrerequisite:

    def __init__(self, course_code, prerequisite_code):
        self.course_code       = course_code        # PK, FK → Course (môn cần học)
        self.prerequisite_code = prerequisite_code  # PK, FK → Course (môn tiên quyết)

    # -------------------------------------------------------------------------
    # CÁC HÀM CRUD – CoursePrerequisite
    # -------------------------------------------------------------------------

    # Lấy toàn bộ bản ghi junction
    @classmethod
    def get_all(cls):
        records = read_file("data/course_prerequisites.txt")
        return [cls(r["course_code"], r["prerequisite_code"]) for r in records]

    # Trả list mã môn tiên quyết của một môn
    @classmethod
    def get_prerequisites_of(cls, course_code):
        return [r.prerequisite_code for r in cls.get_all()
                if r.course_code.upper() == course_code.upper()]

    # Trả list môn nào yêu cầu course_code làm tiên quyết (để kiểm tra trước khi xoá)
    @classmethod
    def get_dependents_of(cls, prerequisite_code):
        return [r.course_code for r in cls.get_all()
                if r.prerequisite_code.upper() == prerequisite_code.upper()]

    # Thêm một cặp (course_code, prerequisite_code). Trả False nếu đã tồn tại
    @classmethod
    def add(cls, course_code, prerequisite_code):
        all_r = cls.get_all()
        for r in all_r:
            if (r.course_code.upper()       == course_code.upper() and
                    r.prerequisite_code.upper() == prerequisite_code.upper()):
                return False  # Đã tồn tại

        records = read_file("data/course_prerequisites.txt")
        records.append({
            "course_code":       course_code,
            "prerequisite_code": prerequisite_code
        })
        write_file("data/course_prerequisites.txt", records)
        return True

    # Xoá một cặp cụ thể. Trả False nếu không tìm thấy
    @classmethod
    def remove(cls, course_code, prerequisite_code):
        records = read_file("data/course_prerequisites.txt")
        new_records = [
            r for r in records
            if not (r.get("course_code",       "").upper() == course_code.upper() and
                    r.get("prerequisite_code",  "").upper() == prerequisite_code.upper())
        ]
        if len(new_records) == len(records):
            return False  # Không tìm thấy

        write_file("data/course_prerequisites.txt", new_records)
        return True

    # Xoá toàn bộ prerequisite liên quan đến một môn (khi xoá Course)
    # Xoá cả 2 chiều: môn này là "course" hoặc là "prerequisite" của môn khác
    @classmethod
    def delete_by_course(cls, course_code):
        records = read_file("data/course_prerequisites.txt")
        records = [
            r for r in records
            if (r.get("course_code",       "").upper() != course_code.upper() and
                r.get("prerequisite_code", "").upper() != course_code.upper())
        ]
        write_file("data/course_prerequisites.txt", records)