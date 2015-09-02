#!/usr/bin/env python
#encoding:utf8

import email  
import mimetypes
from email.MIMEMultipart import MIMEMultipart 
from email.MIMEText import MIMEText  
from email.MIMEImage import MIMEImage  
import smtplib  

class MailSender(object):
    def __init__(self, smtp_server, user, password):
        self.smtp_server = smtp_server
        self.user = user
        self.password = password
        self.login()

    def login(self, smtp_server=None, user=None, password=None):
        self.smtp_server = smtp_server if smtp_server else self.smtp_server
        self.user = user if user else self.user
        self.password = password if password else self.password

        self.smtp = smtplib.SMTP()
        self.smtp.connect(smtp_server)
        self.set_debuglevel(1) # debug level, it depends
        if self.user:
            self.login(user, password)

    def send_mail(self, strFrom, tolist, subject, content):
        strTo = ','.join(tolist)
        msgRoot = MIMEMultipart('related')  
        msgRoot['Subject'] = subject  
        msgRoot['From'] = strFrom  
        msgRoot['To'] = strTo  

        msgAlternative = MIMEMultipart('alternative')  
        msgRoot.attach(msgAlternative)  
        msgText = MIMEText(content, 'html', 'utf-8')
        msgAlternative.attach(msgText) 
        self.smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    
    def quit(self):
        self.smtp.quit()

    def __del__(self):
        self.quit()


