from time import sleep
from gmail import Gmail
from message import Message
from threading import Thread
from ftp import FTPServer, FTPSession
from configuration import Configuration

class Server:

    def __init__(self, credentials, address='0.0.0.0', port=0, forward=False):
        self.forward = forward
        self.gmail = Gmail()
        self.ftp_server = FTPServer(credentials, (address, port), FTPSession)
        self.address, self.port = self.ftp_server.socket.getsockname()

    @property
    def images(self):
        return self.ftp_server.images

    def forward_received_images_on_smtp(self):
        while self.forward:
            sleep(60)

            batch = []
            while not self.images.empty():
                batch.append(self.images.get())
            
            if batch:
                message = Message(Configuration.email_subject, batch)
                self.gmail.connect()
                self.gmail.send(message)
                self.gmail.disconnect()

    def listen(self):
        Thread(target=self.ftp_server.serve_forever).start()
        Thread(target=self.forward_received_images_on_smtp).start()

    def quit(self):
        self.forward = False
        self.ftp_server.shutdown()

if __name__ == '__main__':
    server = Server(
        address=Configuration.address,
        port=Configuration.port,
        credentials=(Configuration.ftp_username, Configuration.ftp_password),
        forward=True
    )
    server.listen()
