import ssl
from email.message import EmailMessage
import smtplib
import imaplib
import json
import time
import os
from typing import List,Dict

from webproject.modules.dotenv_util import get_cwd,initialize_dotenv

servers = {
    "UB":  { "emailServer": "smtp.office365.com", "emailPort": 587, "emailAccount": "cegarcia@bridgeport.edu","password_source":"UBPassword"},
    "DNA": { "emailServer": "smtp.ionos.com", "emailPort": 587, "emailAccount": "cesar@distributedneuralapplications.com","password_source":"NeuroEmail"},
    "LOFT": {"emailServer": "smtp.privateemail.com", "emailPort": 587, "emailAccount":"loft@neurodna.xyz","password_source":"LOFTPassword"}
}
initialize_dotenv()

class UBEmail:
    
    def __init__(self) -> None:
        server = os.environ.get('EMAIL_SERVER')
        
        self.emailServer = servers[server]['emailServer'] #smtp.office365.com
        self.emailPort = servers[server]['emailPort'] #587

        self.password = os.environ.get(servers[server]['password_source'])
        self.emailAccount = servers[server]['emailAccount']

        self.context = ssl.create_default_context()

        self.mailserver = smtplib.SMTP(self.emailServer,self.emailPort)
        self.mailserver.ehlo()
        self.mailserver.starttls()
        self.mailserver.login(self.emailAccount, self.password)

    def send_email(self,recipient,subject,body,carboncopy=None) -> None:
            
            em = EmailMessage()
            recipients = [recipient]
            if carboncopy is not None:
                recipients.append(carboncopy)
            
            em['From'] = self.emailAccount
            em['To'] = recipient
            if carboncopy is not None:
                em['Cc'] = carboncopy
            em['Subject'] = subject

            body = body

            em.set_content(body)
            self.mailserver.sendmail(self.emailAccount,recipients,em.as_string())

            try:
                with imaplib.IMAP4_SSL('mail.privateemail.com') as imap:
                    imap.login(self.emailAccount, self.password)
                    status, response = imap.append("Sent/ub", '\\Seen',imaplib.Time2Internaldate(time.localtime()), em.as_bytes())
            except Exception as e:
                print(f"Error: {e}")
            
            
    def bulk_email(self,emails: List[Dict[str,str]])-> None:
        
        for idx,email in enumerate(emails): 

            self.send_email(recipient=email['email'],subject=email['subject'],body=email['body'])
            
            if idx % 5:
                time.sleep(5)

    # def __del__(self) -> None:
    #     self.mailserver.quit()
