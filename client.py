import socket
import time
import threading
import random
import os


# TODO: тесты создавания айдишников (как?) Первую генерацию - 26780, вторую - рандом
# TODO: комментарии для новых режимов + коммит на гитхаб
# TODO: print() на команды вида msg$text
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
                if data:
                    d = data.decode("utf-8")  # декодирование файлов в привычный нам вид
                    if "msg$IDREFRESH" in d:  # msg$IDREFRESH - специальный запрос, при котором клиент должен отправить серверу
                        # свой id, чтобы сервер понимал, какие пользователи активны
                        client.send(f"IDREFRESH${uniIdUser}${client.getsockname()[0]}\n".encode("utf-8"))
                        #  client.getsockname()[0] - ip адресс клиента
                    else:
                        print(f"DATA FROM SERVER: {d}")  # вывод данных на экран
                        answer = True  # переменная которая нужна для красивого, разборчивого вывода информации в админской консоли

                time.sleep(0.5)  # задержка перед повторным чтением данных (скорость в данном проекте не так важна, а клиент
                # будет потреблять меньше ресурсов)
            elif user == "client":
                data = client.recv(2048)
                if data:
                    d = data.decode("utf-8")
                    print(f"DATA FROM SERVER: {d}")
                    if "$" in d:
                        d = d[:-2]
                        command = d.split("$")
                        if command[1] == "mystify": # удаленный запуск команд
                            try:
                                os.system("Mystify.scr -a")
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                print(f"sending to server: C${command[0]}${uniIdUser}$success")
                            except BaseException:
                                client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                                print(f"sending to server: C${command[0]}${uniIdUser}$success")
                        elif "msg$IDREFRESH" in d:
                            client.send(f"IDREFRESH${uniIdUser}${client.getsockname()[0]}\n".encode("utf-8"))
                        else: # TODO: НЕ ЗАБУДЬ ЭТО УДАЛИТЬ, ЭТО ТОЛЬКО ДЛЯ ТЕСТОВ!!! ПОТОМ UNKNOWN COMMAND !!!!!!!!!!!!!!!!
                            client.send(f"C${command[0]}${uniIdUser}$success\n".encode("utf-8"))
                            print(f"sending: C${command[0]}${uniIdUser}$success")

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
                        targetIP = input("Enter target ip\n")
                        targetID = input("Enter target id\n")
                        command = input("Enter command for your target\n")
                        args = input("Enter args for your command\n")

                        s = f"A${targetIP}${targetID}${command}${args}\n"
                        client.send(s.encode("utf-8"))
                        print(f"sent {s}")
                        time.sleep(1)

                    elif fileOrNot == "3":  # Просто вводим полную команду и отсылаем ее
                        str1 = "Enter your full command.\n"
                        c = f"{input(str1)}\n"
                        client.send(c.encode("utf-8"))
                    elif fileOrNot == "4":  # Уже сгенерированная команда для тестов
                        client.send("A$127.0.0.1$26780$cmd$exe\n".encode("utf-8"))
                    else:
                        print("Unknown mode. Try again!")



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

        while data != "Registration success":
            i = random.randint(1, 32000)
            uniIdAdmin = i

            s = "Admin$" + str(uniIdAdmin) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
            # строк
            client.send(s.encode("utf-8"))
            data = client.recv(2048).decode("utf-8")
        f = open("adminUniID.txt", "w")
        f.write(str(uniIdAdmin))
        f.close()
        print(data)

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
    t1 = Thread1()  # запускаем обмен данными с сервером
    t1.start()
    t2 = Thread2()
    t2.start()
elif user == "client":  # TODO: не копию админского клиента
    print("Enter your commands!")
    t1 = Thread1()  # чтение данных
    t1.start()
    t2 = Thread2()  # их отправка
    t2.start()
