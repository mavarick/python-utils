#!/usr/bin/env python
import smtplib 
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class SimpleMailSender(object):
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.client = smtplib.SMTP(host=host, port=port)

    def send_mail(self, strFrom, tolist, subject, content):
        if isinstance(tolist, type('')):
            strTo = tolist
        else:
            strTo = ','.join(tolist)
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        
        msgText = MIMEText(content)
        msgRoot.attach(msgText)
        self.client.sendmail(strFrom, strTo, msgRoot.as_string())

    def close(self):
        self.client.close()
    
if __name__ == "__main__":
    host = "10.181.10.20"
    port = 25
    sms = SimpleMailSender(host, port)

    #strfrom = "noreply@creditease.cn"
    strfrom = "xufengliu@creditease.cn"

    strto = "xufengliu@creditease.cn"

    sub = "Test"
    content = "this is one test"
    sms.send_mail(strfrom, strto, sub, content)

