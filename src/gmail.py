from smtplib import SMTP
from message import Message
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configuration import Configuration

class Gmail:

    def __init__(self):
        self.credentials = (Configuration.email_username, Configuration.email_password)
        self.connection = SMTP('smtp.gmail.com', 587)

    def connect(self):
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.login(*self.credentials)

    def disconnect(self):
        self.connection.close()

    def send(self, message):
        raw_message = MIMEMultipart()
        raw_message['To'] = message.recipient
        raw_message['From'] = message.sender
        raw_message['Subject'] = message.subject
        raw_message.attach(MIMEImage(message.image, name='image.jpg', _subtype='jpeg'))
        self.connection.sendmail(message.sender, message.recipient, raw_message.as_string())
