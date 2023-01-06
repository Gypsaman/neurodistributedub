import ssl
from email.message import EmailMessage
import smtplib
import json
import time
import os
from typing import List,Dict
servers = {
    "UB":  { "emailServer": "smtp.office365.com", "emailPort": 587, "emailAccount": "cegarcia@brdigeport.edu","password_source":"UBPassword"},
    "DNA": { "emailServer": "smtp.ionos.com", "emailPort": 587, "emailAccount": "cesar@distributedneuralapplications.com","password_source":"NeuroEmail"}
}
class UBEmail:
    
    def __init__(self) -> None:
        self.emailServer = servers["DNA"]['emailServer'] #smtp.office365.com
        self.emailPort = servers["DNA"]['emailPort'] #587

        self.password = os.environ.get(servers["DNA"]['password_source'])
        self.emailAccount = servers["DNA"]['emailAccount']

        self.context = ssl.create_default_context()

        self.mailserver = smtplib.SMTP(self.emailServer,self.emailPort)
        self.mailserver.ehlo()
        self.mailserver.starttls()
        self.mailserver.login(self.emailAccount, self.password)

    def send_email(self,recipient,subject,body) -> None:
            
            em = EmailMessage()

            
            em['From'] = self.emailAccount
            em['To'] = recipient
            em['Subject'] = subject

            body = body

            em.set_content(body)
            self.mailserver.sendmail(self.emailAccount,recipient,em.as_string())
            
            
    def bulk_email(self,emails: List[Dict[str,str]])-> None:
        
        for idx,email in enumerate(emails): 

            self.send_email(recipient=email['email'],subject=email['subject'],body=email['body'])
            
            if idx % 5:
                time.sleep(5)

    def __del__(self) -> None:
        self.mailserver.quit()
