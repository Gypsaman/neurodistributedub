from webproject.modules.ubemail import UBEmail

email = UBEmail()
body = f'testCC'
email.send_email('cegarcia@my.bridgeport.edu','Testing',body,carboncopy='gypsaman@gmail.com')