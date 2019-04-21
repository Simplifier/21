"""
labels
 0 - Name
 1 - Left game
 2 - Stop game
 3 - Start game



"""

import threading
from socket import *
from client_menu import *

#НАСТРОЙКИ СЕТИ
server = ('localhost', 9090)

host = gethostbyname(gethostname())
port = 0
addr = (host, port)

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((host, port))
last_t = 0

def send(data, label):
    data = str(label) + '%%' + data
    #print("send: ", data)
    data = str.encode(data)
    sock.sendto(data, server)


#РЕГИСТРАЦИЯ
start_message()
name = input('Enter your name: ')
send(name, 0)




def receving(name, sock): #Cлушает
    global last_t

    while not stop:
        data, addr = sock.recvfrom(1024)
        data = data.decode("utf-8")
        #print(data)
        last_t, data = data.split("%%")

        if data.find('ROUND')!= -1:
            menuprint(data)
        elif data.find('BEGIN') !=-1:
            menuprint(data)
        elif data.find('END') !=-1:
            menuprint(data)
        else:
            print(data)
            #print(last_t)

stop = False
rT = threading.Thread(target=receving, args=("Boo", sock))
rT.start()


while not stop:
    try:
        data = input()
        if data.lower() in ['stop', 'quit']:
            stop = True

            send("left game", 1)
        elif data.upper() == "START":
            send(data, 3)
        else:
            send(data, last_t)


    except:

        send("close game", 2)
        stop = True

print("\nBye")
sock.close()
