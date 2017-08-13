from gmail import Gmail
from message import Message
from threading import Thread
from ftp import FTPServer, FTPSession

class Server:

    def __init__(self, credentials, address='0.0.0.0', port=0, forward=False):
        self.forward = forward
        self.credentials = credentials
        self.gmail = Gmail()
        self.ftp_server = FTPServer((address, port), FTPSession)
        self.address, self.port = self.ftp_server.socket.getsockname()

    @property
    def images(self):
        return self.ftp_server.images

    def forward_received_images_on_smtp(self):
        while self.forward:
            message = Message('Motion', self.images.get())
            self.gmail.connect()
            self.gmail.send(message)
            self.gmail.disconnect()

    def listen(self):
        Thread(target=self.ftp_server.serve_forever).start()
        Thread(target=self.forward_received_images_on_smtp).start()

if __name__ == '__main__':
    server = Server(address='minkbo.littlist.no', port=1337, credentials=('username', 'password'), forward=True)
    server.listen()
