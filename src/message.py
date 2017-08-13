from configuration import Configuration

class Message:

    def __init__(self, subject, image):
        self.image = image
        self.subject = subject
        self.sender = Configuration.email_username
        self.recipient = Configuration.email_username
