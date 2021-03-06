from smtplib import SMTP
from message import Message
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configuration import Configuration

class Gmail:

    def __init__(self):
        self.credentials = (Configuration.email_username, Configuration.email_password)

    def connect(self):
        self.connection = SMTP('smtp.gmail.com', 587)
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
        raw_message['CC'] = ','.join(message.cc)
        for image in message.images:
            raw_message.attach(MIMEImage(image, name='image.jpg', _subtype='jpeg'))
        self.connection.sendmail(message.sender, [message.recipient] + message.cc, raw_message.as_string())
