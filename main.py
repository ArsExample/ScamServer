import socket
import subprocess
import mouse
import os

def me():
    returned_output = str(subprocess.check_output("whoami"))[2:-1]
    conn.send(returned_output.encode("utf-8"))

def clickLeft():
    mouse.click("left")
def clickRight():
    mouse.click("right")
def shutdown():
    os.system("shutdown -p")
sock = socket.socket()
sock.bind(("", 2345))
sock.listen(1)
conn, address = sock.accept()

while True:
    data = str(conn.recv(1024))[2:-1]
    if not data:
        break
    if data == "me?" or data == "whoami" or data == "me":
        me()
    elif data == "clickLeft" or data == "clkL":
        clickLeft()
    elif data == "clickRight" or data == "clkR":
        clickRight()
    elif data == "shutdown" or data == "sd" or data == "shd":
        shutdown()
sock.close()