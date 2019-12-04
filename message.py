import io
import json
import struct
from socket import socket
from typing import Optional

from protocol_command import ProtocolCommand


class IncomingMessage:
    def __init__(self, sock, con=None) -> None:
        self.con = con
        self.sock: socket = sock

        self._in_buffer = b""
        self.cmd: Optional[ProtocolCommand] = None
        self._size = -1
        self.body = {}
        self.is_loaded = False
        self.is_closed = False

    def read(self):
        self.read_cmd()
        self.read_size()
        self.read_body()

    def read_cmd(self):
        if self.cmd:
            return

        data = self.sock.recv(1)
        if data:
            raw_cmd = struct.unpack(">B", data[:1])[0]
            self.cmd = ProtocolCommand(raw_cmd)
        else:
            self.close()

    def read_size(self):
        if self._size != -1 or self.is_closed:
            return

        data = self.sock.recv(1)
        if data:
            self._size = struct.unpack(">B", data[:1])[0]
            # body is empty
            if self._size == 0:
                self.is_loaded = True

    def read_body(self):
        if self.body or self._size <= 0:
            return

        data = self.sock.recv(self._size - len(self._in_buffer))
        if data:
            self._in_buffer += data

        if len(self._in_buffer) < self._size:
            return

        raw_body = self._in_buffer[:self._size]
        self.body = self._json_decode(raw_body)
        self.is_loaded = True

    def _json_decode(self, json_bytes: bytes):
        obj = json.loads(json_bytes.decode('utf-8'))
        return obj

    def close(self):
        self.is_closed = True
        self.con.close()


class OutgoingMessage:
    def __init__(self, sock) -> None:
        self.sock: socket = sock

    def send(self, command: ProtocolCommand, payload=None):
        data = self.encode(command, payload)
        self.sock.sendall(data)

    def encode(self, command: ProtocolCommand, payload=None):
        cmd = struct.pack(">B", command.value)
        if payload:
            body = self._json_encode(payload)
            size = struct.pack(">B", len(body))
        else:
            body = b''
            size = struct.pack(">B", 0)
        return cmd + size + body

    def _json_encode(self, obj):
        return json.dumps(obj, ensure_ascii=False).encode('utf-8')
