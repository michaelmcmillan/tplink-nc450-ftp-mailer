from unittest import TestCase, skip
from gmail import Gmail
from server import Server
from message import Message
from ftplib import FTP as FTPClient

class FTPLogin(TestCase):

    def test_should_connect_given_correct_credentials(self):
        client = FTPClient()
        server = Server(credentials=('username', 'password'))
        server.listen()
        client.connect(server.address, server.port)
        client.login('username', 'password')

    def test_should_not_connect_given_incorrect_credentials(self):
        client = FTPClient()
        server = Server(credentials=('username', 'password'))
        server.listen()
        client.connect(server.address, server.port)
        with self.assertRaisesRegex(Exception, 'Fuck off'):
            client.login('username', 'drowssap')

    def test_should_not_connect_given_incorrect_username_but_correct_password(self):
        client = FTPClient()
        server = Server(credentials=('username', 'password'))
        server.listen()
        client.connect(server.address, server.port)
        with self.assertRaisesRegex(Exception, 'Fuck off'):
            client.login('emanresu', 'password')

class FTPList(TestCase):

    def test_should_upload_image(self):
        server = Server(credentials=('username', 'password'))
        server.listen()

        client = FTPClient()
        client.connect(server.address, server.port)
        client.login('username', 'password')
        client.storbinary('STOR snapshot.jpg', open('test/snapshot.jpg', 'rb'))

        self.assertEqual(server.images.qsize(), 1)

    def test_should_upload_two_images_from_two_connections(self):
        server = Server(credentials=('username', 'password'))
        server.listen()

        first_client = FTPClient()
        second_client = FTPClient()
        first_client.connect(server.address, server.port)
        second_client.connect(server.address, server.port)
        first_client.login('username', 'password')
        second_client.login('username', 'password')
        first_client.storbinary('STOR snapshot.jpg', open('test/snapshot.jpg', 'rb'))
        second_client.storbinary('STOR snapshot2.jpg', open('test/snapshot2.jpg', 'rb'))
        first_client.quit()
        second_client.quit()

        self.assertEqual(server.images.qsize(), 2)

class TestMail(TestCase):

    @skip('actually connects and tries to send email')
    def test_can_send_mail_with_a_multiple_image(self):
        gmail = Gmail()
        gmail.connect()
        message = Message('Test', [open('test/snapshot.jpg', 'rb').read()]*50)
        gmail.send(message)
        gmail.disconnect()
