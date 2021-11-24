import socket
import subprocess
import mouse
import os

def me():
    returned_output = str(subprocess.check_output("whoami"))[2:-1]
    conn.send(returned_output.encode("utf-8"))

def clickLeft():
    mouse.click("left")
    conn.send("Sucess".encode("utf-8"))
def clickRight():
    mouse.click("right")
    conn.send("Sucess".encode("utf-8"))
def shutdown():
    conn.send("Trying to shutdown server".encode("utf-8"))
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
    else:
        conn.send("Error 1: Unknown command".encode("utf-8"))
sock.close()