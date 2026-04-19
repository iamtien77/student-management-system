from .user_record import UserRecord
from .account import Account
from utils.file_handler import read_file, write_file

DATA_FILE = "data/accounts.txt"

class Admin(UserRecord):
    def __init__(self, cccd, fullName, dob, email, gender, phoneNumber, adminID):
        super().__init__(cccd, fullName, dob, email, gender, phoneNumber)
        self.__adminID = adminID

    def createAccount(self, userInfo):
        account = Account(
            userInfo["username"],
            userInfo["password"],
            userInfo["role"],
            userInfo["intakeYear"],
            userInfo["userRecord"]
        )
        account.save()
        return account

    def manageStudent(self, action, data):
        return True

    def manageLecturer(self, action, data):
        return True

    def manageFaculty(self, action, data):
        return True

    def manageSemester(self, action, data):
        return True

    def manageCourse(self, action, data):
        return True

    def manageClassSection(self, action, data):
        return True

    def assignLecturer(self, lecturer, classSection):
        return True

    def finalizeGrades(self, classSection):
        return True

    def getAdminID(self):
        return self.__adminID

    def __to_line(self) -> str:
        return "|".join([
            self.getCccd(), self.getFullName(), self.getDob(),
            self.getEmail(), self.getGender(), self.getPhoneNumber(),
            self.__adminID
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
            if len(parts) >= 7 and parts[6] == self.__adminID:
                data[i] = self.__to_line()
                updated  = True
                break
        if not updated:
            data.append(self.__to_line())
        write_file(DATA_FILE, data)

    @classmethod
    def getAll(cls) -> list:
        data   = read_file(DATA_FILE)
        result = []
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 7:
                result.append(cls.__from_parts(parts))
        return result