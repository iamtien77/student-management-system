import hashlib
import re
from utils.file_handler import read_file, write_file

DATA_FILE = "data/accounts.txt"

class Account:
    def __init__(self, username, password, role, intakeYear, userRecord):
        self.__username   = username
        self.__password   = self.__hash_password(password)
        self.__role       = role
        self.__intakeYear = intakeYear
        self.__userRecord = userRecord

    def __hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    
    def __is_valid_password(self, pwd):
        return (
            len(pwd) >= 8
            and re.search(r"[A-Z]", pwd)
            and re.search(r"[0-9]", pwd)
            and re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd)
        )

   
    def login(self, username, password):
        return (self.__username == username
                and self.__password == self.__hash_password(password))

    def logout(self) -> None:
        pass  

  
    def changePassword(self, oldPwd, newPwd) :
        if self.__password != self.__hash_password(oldPwd):
            return False
        if not self.__is_valid_password(newPwd):
            raise ValueError("Weak password.")  
        self.__password = self.__hash_password(newPwd)
        self.save()
        return True

   
    def forgotPassword(self, email) -> None:
        if self.__userRecord.getEmail() != email:
            raise ValueError("Email does not match.")
      

   
    def resetPassword(self, newPwd):
        if not self.__is_valid_password(newPwd):
            raise ValueError("Weak password.")
        self.__password = self.__hash_password(newPwd)
        self.save()
        return True

    def getUsername(self):   return self.__username
    def getRole(self):       return self.__role
    def getIntakeYear(self): return self.__intakeYear
    def getUserRecord(self): return self.__userRecord

   
    def __to_line(self) -> str:
        return f"{self.__username}|{self.__password}|{self.__role}|{self.__intakeYear}"

    @classmethod
    def __from_parts(cls, parts: list):
        obj = cls.__new__(cls)          
        obj._Account__username   = parts[0]
        obj._Account__password   = parts[1] 
        obj._Account__role       = parts[2]
        obj._Account__intakeYear = parts[3]
        obj._Account__userRecord = None
        return obj

    def save(self) -> None:
        data    = read_file(DATA_FILE)
        updated = False
        for i, line in enumerate(data):
            parts = line.strip().split("|")
            if parts[0] == self.__username:
                data[i] = self.__to_line()
                updated  = True
                break
        if not updated:
            data.append(self.__to_line())
        write_file(DATA_FILE, data)

    @classmethod
    def getAll(cls) -> list:
        data     = read_file(DATA_FILE)
        accounts = []
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 4:
                accounts.append(cls.__from_parts(parts))  
        return accounts

    @classmethod
    def findById(cls, username: str):
        data = read_file(DATA_FILE)
        for line in data:
            parts = line.strip().split("|")
            if len(parts) >= 4 and parts[0] == username:
                return cls.__from_parts(parts)         
        return None