from socket import *

host = 'localhost'
port = 9090
addr = (host, port)

# настройки сервера
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(addr)
print("[Server started]")