from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn

class FTPServer:

    def __init__(self, credentials, port=None):
        self.credentials = credentials
        self.server = ThreadedTCPServer(('0.0.0.0', port or 0), FTPSession)
        self.address, self.port = self.server.socket.getsockname()

    @property
    def images(self):
        return self.server.images

    def listen(self):
        Thread(target=self.server.serve_forever).start()

class ThreadedTCPServer(ThreadingMixIn, TCPServer):

    def __init__(self, *args):
        self.images = []
        super().__init__(*args)

class FTPSession(BaseRequestHandler):

    def handle(self):
        self.WELCOME()
        while True:
            operation, message = self.get_latest_command()
            if operation and message:
                print(operation, message)
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
        self.servsock.bind(('0.0.0.0', 0))
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
        self.respond(331, 'Provide password.')

    def PASS(self, message):
        if message == 'password':
            self.respond(230, 'Welcome.')
        else:
            self.respond(530, 'Fuck off.')

    def TYPE(self, message):
        self.respond(200, 'Sure')

    def CWD(self, message):
        self.respond(250, 'Sure, you are in the right dir.')

    def MKD(self, message):
        self.respond(200, 'Sure')

    def STOR(self, message):
        data_channel, address = self.servsock.accept()
        self.respond(150, 'Opening data connection.')
        image = self.drain_socket(data_channel)
        self.server.images.append(image) 
        self.respond(226, 'Transfer complete.')
        data_channel.close()

    def PASV(self, message):
        ip, port = self.start_data_channel()
        self.respond(227, 'Entering Passive Mode (%s,%u,%u).' %
            (','.join(ip.split('.')), port >> 8&0xFF, port & 0xFF))

    def QUIT(self, message):
        self.respond(221, 'Bye.')
        #self.servsock.close()

if __name__ == '__main__':
    server = FTPServer(credentials=('username', 'password'))
    print(server.server.socket.getsockname())
    server.listen()
