from webproject.modules.ubemail import UBEmail
import time
from datetime import datetime as dt


def check_submissions():


    for i in range(10):
        email = UBEmail()
        email.send_email('gypsaman@gmail.com','Test',f'It is {dt.now().strptime("%Y-%m-%d %H:%M:%S")}')
        del email
        time.sleep(6*60*60)


if __name__ == '__main__':
    check_submissions()