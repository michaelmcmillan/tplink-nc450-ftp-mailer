# TP-Link NC450 FTP Mailer

Due to the limited number of email alerts on tplinkcloud.com I have 
written a simple FTP server that forwards all motion detection captures
directly to a SMTP server.

Needless to say, the FTP server only implements a small subset of the RFC. Its sole purpose is to receive images from the FTP client on the surveillance camera.

There are no external dependencies, just boot the little guy.

````
python3 src/server.py
````
