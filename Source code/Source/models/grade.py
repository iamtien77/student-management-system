# Lá»›p Grade (Äiá»ƒm) - Ãnh xáº¡ tá»›i D8 (Kho dá»¯ liá»‡u Äiá»ƒm)
# Thuá»™c tÃ­nh: midtermGrade, assignmentGrade, attendanceGrade, finalExamGrade,
#             finalSummaryGrade, letterGrade, trạng thái (Nháp/Đã duyệt)
# PhÆ°Æ¡ng thá»©c: calculateFinalSummary, assignLetterGrade, finalize

from utils.file_handler import (read_records, find_record, find_all_records,
                                 update_record, append_line, write_records)


class Grade:
    # TÃªn file lÆ°u trá»¯ dá»¯ liá»‡u Ä‘iá»ƒm
    FILE = "grades.txt"

    # Trá»ng sá»‘ tÃ­nh Ä‘iá»ƒm tá»•ng káº¿t: giá»¯a ká»³ 20%, bÃ i táº­p 10%, chuyÃªn cáº§n 10%, cuá»‘i ká»³ 60%
    WEIGHT_MIDTERM = 0.20
    WEIGHT_ASSIGNMENT = 0.10
    WEIGHT_ATTENDANCE = 0.10
    WEIGHT_FINAL = 0.60

    def __init__(self, classCode, studentID, midtermGrade=0.0, assignmentGrade=0.0,
                 attendanceGrade=0.0, finalExamGrade=0.0, finalSummaryGrade=0.0,
                 letterGrade="", status="Draft"):
        self._classCode = classCode           # MÃ£ lá»›p há»c pháº§n (FK tá»›i ClassSection)
        self._studentID = studentID           # MÃ£ sinh viÃªn (FK tá»›i Student)
        self._midtermGrade = float(midtermGrade) if midtermGrade else 0.0      # Äiá»ƒm giá»¯a ká»³
        self._assignmentGrade = float(assignmentGrade) if assignmentGrade else 0.0  # Äiá»ƒm bÃ i táº­p
        self._attendanceGrade = float(attendanceGrade) if attendanceGrade else 0.0  # Äiá»ƒm chuyÃªn cáº§n
        self._finalExamGrade = float(finalExamGrade) if finalExamGrade else 0.0    # Äiá»ƒm thi cuá»‘i ká»³
        self._finalSummaryGrade = float(finalSummaryGrade) if finalSummaryGrade else 0.0  # Äiá»ƒm tá»•ng káº¿t
        self._letterGrade = letterGrade       # Äiá»ƒm chá»¯ (A, B, C, D, F)
        self._status = status                 # Tráº¡ng thÃ¡i: Draft (nhÃ¡p) / Finalized (Ä‘Ã£ duyá»‡t)

    # Thuá»™c tÃ­nh

    @property
    def classCode(self):
        return self._classCode

    @property
    def studentID(self):
        return self._studentID

    @property
    def midtermGrade(self):
        return self._midtermGrade

    @property
    def assignmentGrade(self):
        return self._assignmentGrade

    @property
    def attendanceGrade(self):
        return self._attendanceGrade

    @property
    def finalExamGrade(self):
        return self._finalExamGrade

    @property
    def finalSummaryGrade(self):
        return self._finalSummaryGrade

    @property
    def letterGrade(self):
        return self._letterGrade

    @property
    def status(self):
        return self._status

    # PhÆ°Æ¡ng thá»©c theo Class Diagram

    def calculateFinalSummary(self):
        # TÃ­nh Ä‘iá»ƒm tá»•ng káº¿t theo trá»ng sá»‘.
        # Náº¿u chá»‰ cÃ³ giá»¯a ká»³ + cuá»‘i ká»³ (khÃ´ng dÃ¹ng bÃ i táº­p/chuyÃªn cáº§n),
        # Ã¡p dá»¥ng tá»· lá»‡ 30/70 theo tÃ i liá»‡u test case.
        if self._assignmentGrade == 0.0 and self._attendanceGrade == 0.0:
            self._finalSummaryGrade = round(
                self._midtermGrade * 0.30 + self._finalExamGrade * 0.70, 2
            )
            return self._finalSummaryGrade

        self._finalSummaryGrade = round(
            self._midtermGrade * self.WEIGHT_MIDTERM +
            self._assignmentGrade * self.WEIGHT_ASSIGNMENT +
            self._attendanceGrade * self.WEIGHT_ATTENDANCE +
            self._finalExamGrade * self.WEIGHT_FINAL, 2
        )
        return self._finalSummaryGrade

    def assignLetterGrade(self):
        # Chuyá»ƒn Ä‘iá»ƒm tá»•ng káº¿t sang Ä‘iá»ƒm chá»¯ (thang 10)
        score = self._finalSummaryGrade
        if score >= 8.5:
            self._letterGrade = "A"
        elif score >= 7.0:
            self._letterGrade = "B"
        elif score >= 5.5:
            self._letterGrade = "C"
        elif score >= 4.0:
            self._letterGrade = "D"
        else:
            self._letterGrade = "F"
        return self._letterGrade

    def finalize(self):
        # KhÃ³a Ä‘iá»ƒm vÄ©nh viá»…n, sau khi duyá»‡t khÃ´ng thá»ƒ sá»­a Ä‘á»•i
        if self._status == "Finalized":
            return False
        self._status = "Finalized"
        self.save()
        return True

    # Chuyá»ƒn Ä‘á»•i dá»¯ liá»‡u

    def to_record(self):
        return [self._classCode, self._studentID,
                str(self._midtermGrade), str(self._assignmentGrade),
                str(self._attendanceGrade), str(self._finalExamGrade),
                str(self._finalSummaryGrade), self._letterGrade, self._status]

    @staticmethod
    def from_record(record):
        if len(record) >= 9:
            return Grade(*record[:9])
        return None

    def save(self):
        # LÆ°u hoáº·c cáº­p nháº­t báº£n ghi Ä‘iá»ƒm
        # KhÃ³a chÃ­nh lÃ  cáº·p (classCode, studentID)
        records = read_records(self.FILE)
        updated = False
        for i, r in enumerate(records):
            if len(r) >= 2 and r[0] == self._classCode and r[1] == self._studentID:
                records[i] = self.to_record()
                updated = True
                break
        if updated:
            return write_records(self.FILE, records)
        return append_line(self.FILE, "|".join(self.to_record()))

    @staticmethod
    def find_by_student_class(student_id, class_code):
        # TÃ¬m Ä‘iá»ƒm cá»§a má»™t sinh viÃªn trong má»™t lá»›p cá»¥ thá»ƒ
        for r in read_records(Grade.FILE):
            if len(r) >= 2 and r[0] == class_code and r[1] == student_id:
                return Grade.from_record(r)
        return None

    @staticmethod
    def find_by_student(student_id):
        # TÃ¬m táº¥t cáº£ Ä‘iá»ƒm cá»§a má»™t sinh viÃªn
        records = find_all_records(Grade.FILE, 1, student_id)
        return [Grade.from_record(r) for r in records if Grade.from_record(r) is not None]

    @staticmethod
    def find_by_class(class_code):
        # TÃ¬m táº¥t cáº£ Ä‘iá»ƒm trong má»™t lá»›p há»c pháº§n
        records = find_all_records(Grade.FILE, 0, class_code)
        return [Grade.from_record(r) for r in records if Grade.from_record(r) is not None]

    @staticmethod
    def get_all():
        return [Grade.from_record(r) for r in read_records(Grade.FILE)
                if Grade.from_record(r) is not None]

