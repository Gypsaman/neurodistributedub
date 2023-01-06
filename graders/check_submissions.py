from webproject.modules.ubemail import UBEmail
import time


def check_submissions():
    email = UBEmail()

    for i in range(10):
        email.send_email('gypsaman@gmail.com','Test','This is a test')
        time.sleep(10*60)


if __name__ == '__main__':
    check_submissions()