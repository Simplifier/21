import selectors
import socket

from client_connection import Connection

sel = selectors.DefaultSelector()


def start_connection(host, port):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    con = Connection(sel, sock, addr)
    sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, con)
    return con


if __name__ == "__main__":
    host, port = '127.0.0.1', 9090
    con = start_connection(host, port)
    con.entry()

    while True:
        try:
            events = sel.select(timeout=1)
            for key, mask in events:
                con.process_events(mask)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
        except OSError:
            print('Connection closed before opening')
            break
