from utils.file_handler import read_file, write_file

DATA_FILE = "data/faculties.txt"

class Faculty:
    def __init__(self, facultyCode, facultyName, email, phoneNumber):
        self.__facultyCode  = facultyCode
        self.__facultyName  = facultyName
        self.__email        = email
        self.__phoneNumber  = phoneNumber

    def getFacultyCode(self):   return self.__facultyCode
    def getFacultyName(self):   return self.__facultyName
    def getEmail(self):         return self.__email
    def getPhoneNumber(self):   return self.__phoneNumber

    def __to_line(self):
        return "|".join([
            self.__facultyCode, self.__facultyName,
            self.__email, self.__phoneNumber
        ])

    @classmethod
    def __from_parts(cls, parts: list):
        return cls(parts[0], parts[1], parts[2], parts[3])

    def save(self):
        data    = read_file(DATA_FILE)
        updated = False
        for i, line in enumerate(data):
            parts = line.strip().split("|")
            if len(parts) >= 4 and parts[0] == self.__facultyCode:
                data[i] = self.__to_line()
                updated  = True
                break
        if not updated:
            data.append(self.__to_line())
        write_file(DATA_FILE, data)

    @classmethod
    def findById(cls, facultyCode: str):
        data = read_file(DATA_FILE)
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 4 and parts[0] == facultyCode:
                return cls.__from_parts(parts)
        return None

    @classmethod
    def getAll(cls):
        data   = read_file(DATA_FILE)
        result = []
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 4:
                result.append(cls.__from_parts(parts))
        return result