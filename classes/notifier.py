import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from .logger import Logger
import os

logger = Logger("Mailer")


class Mailer:
    def __init__(self, *args, **kwargs):
        self.sender = os.environ['SENDER']
        self.password = os.environ['PASSWORD']
        self.receiver_phone = os.environ['RECIEVER']
        self.smtp_server = 'smtp.gmail.com'
        self.TLS_port = 587

    def sendMessage(self, message):
        try:
            session = smtplib.SMTP(self.smtp_server, self.TLS_port)
            session.starttls()
            session.login(self.sender, self.password)
            session.sendmail(self.sender, self.receiver_phone, message)
            session.quit()
            logger.info(f'Text sent, message - {message}')
        except Exception as e:
            logger.error(e)
            logger.error('Could not send notification text')
