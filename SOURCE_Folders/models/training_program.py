# models/training_program.py  –  Chương trình đào tạo
# Tách thành 2 file dữ liệu khớp với data model:
#   data/training_programs.txt  → thông tin chương trình (program_id, program_name, faculty_code)
#   data/program_courses.txt    → junction table ProgramCourse (program_id, course_code)

from utils.file_handler import read_file, write_file


class TrainingProgram:

    def __init__(self, program_id, program_name, faculty_code):
        self.program_id   = program_id    # PK - Mã chương trình (VD: CNTT2022)
        self.program_name = program_name  # Tên chương trình
        self.faculty_code = faculty_code  # FK - Mã khoa quản lý

    # -------------------------------------------------------------------------
    # CÁC HÀM CRUD – TrainingProgram (tương tác với training_programs.txt)
    # -------------------------------------------------------------------------

    # Lấy toàn bộ danh sách chương trình đào tạo
    @classmethod
    def get_all(cls):
        records = read_file("data/training_programs.txt")
        return [cls(
            program_id=r["program_id"],
            program_name=r["program_name"],
            faculty_code=r["faculty_code"]
        ) for r in records]

    # Tìm chương trình theo mã
    @classmethod
    def find_by_id(cls, program_id):
        for p in cls.get_all():
            if p.program_id.upper() == program_id.upper():
                return p
        return None

    # Lấy danh sách chương trình thuộc một khoa
    @classmethod
    def find_by_faculty(cls, faculty_code):
        return [p for p in cls.get_all()
                if p.faculty_code.upper() == faculty_code.upper()]

    # Lưu hoặc cập nhật chương trình đào tạo (chỉ lưu thông tin chính, không lưu courses ở đây)
    def save(self):
        records = read_file("data/training_programs.txt")
        new_record = {
            "program_id":   self.program_id,
            "program_name": self.program_name,
            "faculty_code": self.faculty_code
        }

        updated = False
        for i, r in enumerate(records):
            if r.get("program_id") == self.program_id:
                records[i] = new_record
                updated = True
                break

        if not updated:
            records.append(new_record)

        write_file("data/training_programs.txt", records)
        return True

    # Xoá chương trình và toàn bộ môn liên kết trong junction table
    @classmethod
    def delete(cls, program_id):
        records = read_file("data/training_programs.txt")
        records = [r for r in records if r.get("program_id") != program_id]
        write_file("data/training_programs.txt", records)

        # Xoá các dòng liên quan trong junction table ProgramCourse
        ProgramCourse.delete_by_program(program_id)
        return True

    # True nếu mã chương trình đã tồn tại
    def is_duplicate(self):
        return self.find_by_id(self.program_id) is not None

    # -------------------------------------------------------------------------
    # LOGIC NGHIỆP VỤ
    # -------------------------------------------------------------------------

    # Lấy danh sách mã môn thuộc chương trình này (query sang junction table)
    def get_courses(self):
        return ProgramCourse.get_courses_of_program(self.program_id)

    # So sánh danh sách môn trong chương trình với môn sinh viên đã hoàn thành.
    # completed_course_codes: list mã môn sinh viên đã qua (lấy từ Grade.get_completed_courses)
    def get_completion_status(self, completed_course_codes):
        all_courses = self.get_courses()          # danh sách mã môn của chương trình
        done_set    = {c.upper() for c in completed_course_codes}

        completed  = [c for c in all_courses if c.upper() in done_set]
        incomplete = [c for c in all_courses if c.upper() not in done_set]

        return {
            "completed":   completed,
            "incomplete":  incomplete,
            "total":       len(all_courses),
            "done_count":  len(completed),
        }

    def __str__(self):
        return (f"[{self.program_id}] {self.program_name} "
                f"| Khoa: {self.faculty_code}")


# =============================================================================
# Junction table: ProgramCourse  (program_id  <-->  course_code)
# Tương đương bảng ProgramCourse trong data model / drawio diagram
# File lưu trữ: data/program_courses.txt
# =============================================================================

class ProgramCourse:

    def __init__(self, program_id, course_code):
        self.program_id  = program_id   # PK, FK → TrainingProgram
        self.course_code = course_code  # PK, FK → Course

    # -------------------------------------------------------------------------
    # CÁC HÀM CRUD – ProgramCourse
    # -------------------------------------------------------------------------

    # Lấy toàn bộ bản ghi junction
    @classmethod
    def get_all(cls):
        records = read_file("data/program_courses.txt")
        return [cls(r["program_id"], r["course_code"]) for r in records]

    # Trả list mã môn thuộc một chương trình
    @classmethod
    def get_courses_of_program(cls, program_id):
        return [r.course_code for r in cls.get_all()
                if r.program_id.upper() == program_id.upper()]

    # Trả list mã chương trình có chứa một môn học
    @classmethod
    def get_programs_of_course(cls, course_code):
        return [r.program_id for r in cls.get_all()
                if r.course_code.upper() == course_code.upper()]

    # Thêm một môn vào chương trình. Trả False nếu cặp (program_id, course_code) đã tồn tại
    @classmethod
    def add(cls, program_id, course_code):
        all_r = cls.get_all()
        for r in all_r:
            if (r.program_id.upper()  == program_id.upper() and
                    r.course_code.upper() == course_code.upper()):
                return False  # Đã tồn tại, không thêm trùng

        records = read_file("data/program_courses.txt")
        records.append({"program_id": program_id, "course_code": course_code})
        write_file("data/program_courses.txt", records)
        return True

    # Xoá một môn khỏi chương trình. Trả False nếu không tìm thấy
    @classmethod
    def remove(cls, program_id, course_code):
        records = read_file("data/program_courses.txt")
        new_records = [
            r for r in records
            if not (r.get("program_id",  "").upper() == program_id.upper() and
                    r.get("course_code", "").upper() == course_code.upper())
        ]
        if len(new_records) == len(records):
            return False  # Không tìm thấy cặp này

        write_file("data/program_courses.txt", new_records)
        return True

    # Xoá toàn bộ môn của một chương trình (dùng khi xoá TrainingProgram)
    @classmethod
    def delete_by_program(cls, program_id):
        records = read_file("data/program_courses.txt")
        records = [r for r in records if r.get("program_id") != program_id]
        write_file("data/program_courses.txt", records)

    # Xoá toàn bộ liên kết của một môn học (dùng khi Admin xoá Course)
    @classmethod
    def delete_by_course(cls, course_code):
        records = read_file("data/program_courses.txt")
        records = [r for r in records if r.get("course_code") != course_code]
        write_file("data/program_courses.txt", records)