import socket
import time
import threading
import random
import os

# admin -> client
# 127.0.0.1$26780$cmd$exe
# admin <- client
# 127.0.0.1$26780$22100$1$cmd$exe

client = socket.socket() # создаем объект клиента
#  print(socket.gethostbyname(socket.gethostname()))

user = input("admin or client? \n")  # тестовый вариант!! выбираем, кем будет являться наш пользователь

answer = False

u = "utf-8"

class Thread1(threading.Thread): # потоки через класс тк threading.Thread(target=...) не работает
    def run(self):
        global answer
        while True: # бесконечный цикл с приемом данных (в отдельном потоке)
            data = client.recv(2048)
            if data:
                d = data.decode("utf-8")  # декодирование файлов в привычный нам вид
                print(f"DATA FROM SERVER: {d}")  # вывод данных на экран
                answer = True
            time.sleep(0.5)


class Thread2(threading.Thread):  # поток для бесконечной отправки данных на сервер (когда нам надо)
    def run(self):
        global user
        global answer
        global u
        while True:
            if user == "admin":
                while True:
                    while not answer:
                        time.sleep(1)
                    time.sleep(1)
                    fileOrNot = input("----------------------------------------------------------\n"
                                      "Do you want to start existing script (1) or to make it now (2)?\n"
                                      " Also you can use advanced mode (3).\n"
                                      "----------------------------------------------------------\n")
                    if fileOrNot == "1":
                        f = open("file.script")
                        lines = f.readlines()
                        delay = False
                        for i in range(int(lines[0][10]) * 2):
                            if delay:
                                time.sleep(int(lines[i + 1]))
                                delay = False
                                continue
                            if not delay:
                                client.send(f"{lines[i + 1]}\n".encode("utf-8"))
                                print("sending!")
                                delay = True
                                continue
                    elif fileOrNot == "2":
                        targetIP = input("Enter target ip\n")
                        targetID = input("Enter target id\n")
                        command = input("Enter command for your target\n")
                        args = input("Enter args for your command\n")


                        s = f"A${targetIP}${targetID}${command}${args}\n"  # добавляем специальный префикс админа
                        client.send(s.encode("utf-8"))
                        print(f"senden {s}")

                        answer = False
                    elif fileOrNot == "3":
                        break
                    else:
                        print("Unknown mode. Try again!")


            elif user == "client":
                u = "utf-8"
                s = "C$" + input() + "\n"  # добавляем специальный префикс клиента
                client.send(s.encode("utf-8"))
                print(f"senden {s}")
                print(f"senden-encoden(wtf) {s.encode(u)}")


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

        print("начало цикла")
        if "Registration success" not in data:
            print("после ифа")
            while data != "Registration success\n":
                i = random.randint(1, 32000)
                uniIdUser = i

                s = "Client$" + str(uniIdUser) + "\n"  # отправляем на сервер специальную строку. ВАЖНО!!! после всех
                # строк
                client.send(s.encode("utf-8"))
                data = client.recv(2048).decode("utf-8")
            print("после цикла в ифе")
        print("конец цикла")
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
