from configuration import Configuration

class Message:

    def __init__(self, subject, images):
        self.images = images
        self.subject = subject
        self.sender = Configuration.email_username
        self.recipient = Configuration.email_username
