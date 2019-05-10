from protocol_command import ProtocolCommand


class Player:
    def __init__(self, name, con):
        self.name = name
        self.con = con
        self.points = 0

    def send(self, command: ProtocolCommand, payload=None):
        self.con.out_msg.send(command, payload)

    def __str__(self):
        return self.name
