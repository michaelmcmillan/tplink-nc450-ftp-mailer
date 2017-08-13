from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn

class FTPServer(ThreadingMixIn, TCPServer):

    def __init__(self, credentials, address, handler):
        self.images = Queue()
        self.address = address
        self.credentials = credentials
        super().__init__(address, handler)

class FTPSession(BaseRequestHandler):

    def handle(self):
        self.authenticated = False
        self.WELCOME()
        while True:
            operation, message = self.get_latest_command()
            if not operation: continue
            method = getattr(self, operation)
            method(message)

    def get_latest_command(self):
        data = self.request.recv(1024).decode()
        operation, *message = data.split(' ', 1)
        return operation.rstrip(), ' '.join(message).rstrip()

    def respond(self, operation, message):
        response = ('%d %s\r\n' % (operation, message)).encode('utf-8')
        self.request.sendall(response)

    def start_data_channel(self):
        self.servsock = socket(AF_INET, SOCK_STREAM)
        ip, port = self.server.address
        self.servsock.bind((ip, 0))
        self.servsock.listen(1)
        return self.servsock.getsockname()

    def drain_socket(self, socket):
        received_data = bytearray()
        while True:
            chunk = socket.recv(1024)
            received_data.extend(chunk)
            if not chunk:
                break
        return received_data

    def WELCOME(self):
        self.respond(220, 'Welcome!')

    def USER(self, message):
        username, password = self.server.credentials
        if message == username:
            self.respond(331, 'Provide password.')
        else:
            self.respond(530, 'Fuck off.')

    def PASS(self, message):
        username, password = self.server.credentials
        if message == password:
            self.authenticated = True
            self.respond(230, 'Welcome.')
        else:
            self.respond(530, 'Fuck off.')

    def TYPE(self, message):
        self.respond(200, 'Sure')

    def CWD(self, message):
        self.respond(250, 'Sure, you are in the right dir.')

    def SIZE(self, message):
        self.respond(550, 'Nope, no such file.')

    def MKD(self, message):
        self.respond(200, 'Sure')

    def STOR(self, message):
        if not self.authenticated:
            return
        data_channel, address = self.servsock.accept()
        self.respond(150, 'Opening data connection.')
        image = self.drain_socket(data_channel)
        self.server.images.put(image)
        self.respond(226, 'Transfer complete.')
        data_channel.close()

    def PASV(self, message):
        if not self.authenticated:
            return
        ip, port = self.start_data_channel()
        self.respond(227, 'Entering Passive Mode (%s,%u,%u).' %
            (','.join(ip.split('.')), port >> 8&0xFF, port & 0xFF))

    def QUIT(self, message):
        self.respond(221, 'Bye.')
