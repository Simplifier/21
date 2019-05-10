import selectors
import socket

from server_connection import Connection

sel = selectors.DefaultSelector()
game_rooms = {}  # все игры


def accept_connection(sock: socket.socket):
    con, addr = sock.accept()
    print('accepted connection from', addr)
    con.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(con, events, Connection(sel, con, addr, game_rooms))


if __name__ == "__main__":
    host, port = '', 9090
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    print("listening on", (host, port))
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ)

    while True:
        events = sel.select()
        for key, mask in events:
            if key.data is None:
                accept_connection(key.fileobj)
            else:
                con = key.data
                con.process_events(mask)
