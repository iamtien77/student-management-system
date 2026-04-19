from .user_record import UserRecord
from .training_program import TrainingProgram
from utils.file_handler import read_file, write_file

DATA_FILE = "data/students.txt"

class Student(UserRecord):
    def __init__(self, cccd, fullName, dob, email, gender, phoneNumber,
                 studentID, programID, status):
        super().__init__(cccd, fullName, dob, email, gender, phoneNumber)
        self.__studentID     = studentID
        self.__programID     = programID
        self.__status        = status
        self.__grades        = []
        self.__semesterGPA   = 0.0
        self.__cumulativeGPA = 0.0

    def viewTrainingProgram(self):
        return TrainingProgram.findById(self.__programID)

    def viewGrades(self):
        return self.__grades

    def viewGPA(self):
        return self.calculateCumulativeGPA()

    def calculateSemesterGPA(self):
        if not self.__grades:
            return 0.0
        total = sum(score for _, score, _ in self.__grades)
        self.__semesterGPA = total / len(self.__grades)
        return self.__semesterGPA

    def calculateCumulativeGPA(self):
        if not self.__grades:
            return 0.0
        totalPoints, totalCredits = 0, 0
        for _, score, credits in self.__grades:
            totalPoints += score * credits
            totalCredits += credits
        self.__cumulativeGPA = totalPoints / totalCredits if totalCredits else 0.0
        return self.__cumulativeGPA

    def getStudentID(self):      return self.__studentID
    def getProgramID(self):      return self.__programID
    def getStatus(self):         return self.__status
    def getSemesterGPA(self):    return self.__semesterGPA
    def getCumulativeGPA(self):  return self.__cumulativeGPA

    def __to_line(self):
        return "|".join([
            self.getCccd(), self.getFullName(), self.getDob(),
            self.getEmail(), self.getGender(), self.getPhoneNumber(),
            self.__studentID, self.__programID, self.__status
        ])

    @classmethod
    def __from_parts(cls, parts: list):
        return cls(parts[0], parts[1], parts[2],
                   parts[3], parts[4], parts[5],
                   parts[6], parts[7], parts[8])

    def save(self) -> None:
        data    = read_file(DATA_FILE)
        updated = False
        for i, line in enumerate(data):
            parts = line.strip().split("|")
            if len(parts) >= 9 and parts[6] == self.__studentID:
                data[i] = self.__to_line()
                updated  = True
                break
        if not updated:
            data.append(self.__to_line())
        write_file(DATA_FILE, data)

    @classmethod
    def findById(cls, studentID: str):
        data = read_file(DATA_FILE)
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 9 and parts[6] == studentID:
                return cls.__from_parts(parts)
        return None

    @classmethod
    def getAll(cls):
        data   = read_file(DATA_FILE)
        result = []
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 9:
                result.append(cls.__from_parts(parts))
        return result