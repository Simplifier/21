import selectors
from random import randint
from socket import socket
from typing import Optional

import deck
from game_room import GameRoom
from player import Player
from message import IncomingMessage, OutgoingMessage
from protocol_command import ProtocolCommand


class Connection:
    def __init__(self, selector, sock, addr, game_rooms):
        self.game_rooms = game_rooms
        self.selector = selector
        self.sock: socket = sock
        self.addr = addr

        self.in_msg = IncomingMessage(sock, self)
        self.out_msg = OutgoingMessage(sock)
        self.player: Optional[Player] = None
        self.game: Optional[GameRoom] = None
        self.cmd_handlers = {
            ProtocolCommand.SEND_NAME: self.create_player,
            ProtocolCommand.NEW_ROOM: self.create_game,
            ProtocolCommand.JOIN_ROOM: lambda: self.out_msg.send(ProtocolCommand.WAIT_PASS),
            ProtocolCommand.SEND_PASS: self.handle_join_try,
            ProtocolCommand.START_GAME: self.start_game,
            ProtocolCommand.TAKE_CARD: self.make_turn,
        }

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()

    def read(self):
        if self.in_msg.is_loaded:
            self.in_msg = IncomingMessage(self.sock, self)
        self.in_msg.read()

        if not self.in_msg.is_loaded:
            return

        print(f'cmd: {self.in_msg.cmd}, args: {self.in_msg.body}, from: {self.addr}, {self.player}')

        self.cmd_handlers[self.in_msg.cmd](**self.in_msg.body)

    def create_player(self, name):
        self.player = Player(name, self)
        return self.player

    def create_game(self):
        password = randint(1000, 10000)
        self.game = GameRoom(self.player, password)
        self.game_rooms[password] = self.game
        self.out_msg.send(ProtocolCommand.PASS_CREATED, {
            'password': self.game.password
        })

    def handle_join_try(self, password):
        game: GameRoom = self.game_rooms.get(password, None)
        if game:
            game.add_player(self.player)
            self.game = game
            self.out_msg.send(ProtocolCommand.ACCEPT_JOIN, {
                'participants': list(map(lambda p: p.name, game.players))
            })
            game.send_to_all_except(self.player, ProtocolCommand.PLAYER_JOINED, {
                'player_name': self.player.name
            })

            if len(game.players) == 2:
                game.admin.send(ProtocolCommand.GAME_CAN_BEGIN)
        else:
            self.out_msg.send(ProtocolCommand.REJECT_JOIN)

    def start_game(self):
        self._start_round()

    def _start_round(self):
        self.game.made_choice_count = 0
        self.game.round += 1
        for i, p in enumerate(self.game.active_players):
            p.send(ProtocolCommand.ROUND_STARTED, {
                'round': self.game.round,
                'points': p.points,
                'player_name': p.name
            })

    def make_turn(self, take_card):
        self.game.made_choice_count += 1
        if take_card:
            self._take_card()

        self.game.send_to_all_except(self.player, ProtocolCommand.PLAYER_TURNED, {
            'player_name': self.player.name
        })

        if self.game.made_choice_count == len(self.game.active_players):
            self._handle_winners_and_losers()
            self._start_round()

    def _take_card(self):
        card = deck.get_random_card()
        self.player.points += card.points
        self.out_msg.send(ProtocolCommand.CARD_TAKEN, {
            'suit': card.suit,
            'rank': card.rank,
            'points': self.player.points
        })

    def _handle_winners_and_losers(self):
        winner_found = False
        for i, p in enumerate(self.game.active_players):
            if p.points == 21:
                self._player_wins(p)
                winner_found = True
            elif p.points > 21:
                self._player_loses(p)

        if len(self.game.active_players) == 1:
            if winner_found:
                self._player_loses(self.game.active_players[0])
            else:
                self._player_wins(self.game.active_players[0])

        if len(self.game.active_players) == 0:
            self.game.send_to_all(ProtocolCommand.GAME_OVER)

    def _player_wins(self, player):
        player.send(ProtocolCommand.YOU_WIN)
        self.game.send_to_all_except(player, ProtocolCommand.PLAYER_WINS, {
            'player_name': player.name,
            'points': player.points
        })
        self.game.deactivate_player(player)

    def _player_loses(self, player):
        player.send(ProtocolCommand.YOU_LOSE)
        self.game.send_to_all_except(player, ProtocolCommand.PLAYER_LOSES, {
            'player_name': player.name,
            'points': player.points
        })
        self.game.deactivate_player(player)

    def close(self):
        print("closing connection to", self.addr)
        if self.game:
            self.game.remove_player(self.player)
        self.selector.unregister(self.sock)
        self.sock.close()
