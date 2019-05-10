from player import Player
from protocol_command import ProtocolCommand


class GameRoom:
    def __init__(self, player: Player, password):
        self.admin = player
        self.password = password
        self.players = [player]
        self.active_players = [player]
        self.round = 0
        self.made_choice_count = 0

    def add_player(self, player):
        self.players.append(player)
        self.active_players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        self.deactivate_player(player)

    def deactivate_player(self, player):
        if player in self.active_players:
            self.active_players.remove(player)

    def send_to_all(self, command: ProtocolCommand, payload=None):
        for player in self.players:
            player.send(command, payload)

    def send_to_all_except(self, player: Player, command: ProtocolCommand, payload=None):
        for p in self.players:
            if p != player:
                p.send(command, payload)