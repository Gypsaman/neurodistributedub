from enum import Enum
from datetime import datetime as dt

class LogType(Enum):
    LOGIN = 1
    PASSWORD = 2
    QUIZ = 3
    ASSIGNMENT = 4
    REGISTER = 5
    ERROR = 6
    
    
def Log(log_type, user, message):
    with open("log.txt", "a") as f:
        f.write(f"{log_type.name},{dt.now().strftime('%Y-%m-%d %H:%M')},{user},{message}\n")

if __name__ == "__main__":
    Log(LogType.LOGIN, "admin", "admin logged in")