from utils.file_handler import read_file, write_file

class UserRecord:
    def __init__(self, cccd, fullName, dob, email, gender, phoneNumber):
        self.__cccd        = cccd
        self.__fullName    = fullName
        self.__dob         = dob
        self.__email       = email
        self.__gender      = gender
        self.__phoneNumber = phoneNumber

    def updatePersonalInfo(self, email, phoneNumber):
        self.__email       = email
        self.__phoneNumber = phoneNumber
        self.save() 
        return True

    def getCccd(self):        return self.__cccd
    def getFullName(self):    return self.__fullName
    def getDob(self):         return self.__dob
    def getEmail(self):       return self.__email
    def getGender(self):      return self.__gender
    def getPhoneNumber(self): return self.__phoneNumber