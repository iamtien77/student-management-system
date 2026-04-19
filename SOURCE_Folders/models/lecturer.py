from .user_record import UserRecord
from utils.file_handler import read_file, write_file

DATA_FILE = "data/lecturers.txt"

class Lecturer(UserRecord):
    def __init__(self, cccd, fullName, dob, email, gender, phoneNumber, employeeID):
        super().__init__(cccd, fullName, dob, email, gender, phoneNumber)
        self.__employeeID = employeeID

    def takeAttendance(self, classSection, student, status):
        return True

    def inputComponentGrades(self, student, grades):
        return True

    def inputFinalExamGrade(self, student, grade):
        return True

    def saveDraft(self):
        return True

    def getEmployeeID(self):
        return self.__employeeID

    def __to_line(self):
        return "|".join([
            self.getCccd(), self.getFullName(), self.getDob(),
            self.getEmail(), self.getGender(), self.getPhoneNumber(),
            self.__employeeID
        ])

    @classmethod
    def __from_parts(cls, parts: list):
        return cls(parts[0], parts[1], parts[2],
                   parts[3], parts[4], parts[5], parts[6])

    def save(self) -> None:
        data    = read_file(DATA_FILE)
        updated = False
        for i, line in enumerate(data):
            parts = line.strip().split("|")
            if len(parts) >= 7 and parts[6] == self.__employeeID:
                data[i] = self.__to_line()
                updated  = True
                break
        if not updated:
            data.append(self.__to_line())
        write_file(DATA_FILE, data)

    @classmethod
    def findById(cls, employeeID: str):
        data = read_file(DATA_FILE)
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 7 and parts[6] == employeeID:
                return cls.__from_parts(parts)
        return None

    @classmethod
    def getAll(cls) -> list:
        data   = read_file(DATA_FILE)
        result = []
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 7:
                result.append(cls.__from_parts(parts))
        return result