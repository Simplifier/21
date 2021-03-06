import selectors
from socket import socket

from cards import Card, front_card
from menu import show_rules, menu_print
from message import IncomingMessage, OutgoingMessage
from protocol_command import ProtocolCommand


class Connection:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock: socket = sock
        self.addr = addr
        self.in_msg: IncomingMessage = IncomingMessage(sock)
        self.out_msg: OutgoingMessage = OutgoingMessage(sock)
        self.cmd_handlers = {
            ProtocolCommand.PASS_CREATED: self.host_received_password,
            ProtocolCommand.WAIT_PASS: self.companion_send_password,
            ProtocolCommand.REJECT_JOIN: self.companion_rejected,
            ProtocolCommand.ACCEPT_JOIN: self.companion_joined,
            ProtocolCommand.PLAYER_JOINED: self.show_joined_player,
            ProtocolCommand.GAME_CAN_BEGIN: self.start_game,
            ProtocolCommand.ROUND_STARTED: self.start_round,
            ProtocolCommand.CARD_TAKEN: self.receive_card,
            ProtocolCommand.PLAYER_TURNED: self.show_choice_notification,
            ProtocolCommand.YOU_WIN: self.you_win,
            ProtocolCommand.PLAYER_WINS: self.someone_wins,
            ProtocolCommand.YOU_LOSE: self.you_lose,
            ProtocolCommand.PLAYER_LOSES: self.someone_loses,
            ProtocolCommand.GAME_OVER: self.game_over,
        }

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()

    def read(self):
        if self.in_msg.is_loaded:
            self.in_msg = IncomingMessage(self.sock)
        self.in_msg.read()

        if not self.in_msg.is_loaded:
            return

        self.cmd_handlers[self.in_msg.cmd](**self.in_msg.body)

    def entry(self):
        show_rules()
        name = input('Enter your name: ')
        if self.read_quit(name):
            return

        self.out_msg.send(ProtocolCommand.SEND_NAME, {'name': name})
        self.create_or_join_game_room()

    def create_or_join_game_room(self):
        print('Do you want to start a NEW game or JOIN an existing game? [n]ew/[j]oin\n')
        answer = input().lower()
        if self.read_quit(answer):
            return

        if answer in ('n', 'new'):
            self.out_msg.send(ProtocolCommand.NEW_ROOM)
        elif answer in ('j', 'join'):
            self.out_msg.send(ProtocolCommand.JOIN_ROOM)
        else:
            print('Unknown input. Please repeat')
            self.create_or_join_game_room()

    def host_received_password(self, password):
        print('You created a new game')
        print('Wait other players')
        print('Game password:', password)
        print('Send it to your companions, who want to join the game')

    def companion_send_password(self):
        print('Enter game password')
        raw_pass = input().lower()
        if self.read_quit(raw_pass):
            return

        if self._is_int(raw_pass):
            self.out_msg.send(ProtocolCommand.SEND_PASS, {'password': int(raw_pass)})
        else:
            print('Password should be a number. Please retry')
            self.companion_send_password()

    def _is_int(self, value: str):
        try:
            int(value)
            return True
        except:
            return False

    def companion_rejected(self):
        print('Password is incorrect. Please retry')
        self.companion_send_password()

    def companion_joined(self, participants):
        print('You have successfully connected to the game')
        print('Participants:')
        list(map(print, participants))
        print('Wait until game starts')

    def show_joined_player(self, player_name):
        print('New player joins the game:', player_name)

    def start_game(self):
        print('Type [s]tart when you are ready')
        answer = input().lower()
        if self.read_quit(answer):
            return

        if answer in ('s', 'start'):
            self.out_msg.send(ProtocolCommand.START_GAME)
        else:
            print('Unknown input. Please repeat')
            self.start_game()

    def start_round(self, round, points, player_name):
        print()
        if round == 1:
            menu_print('BEGIN GAME')

        menu_print(f"ROUND {round}")
        print('#' * 50)
        print(f'|###{player_name}  Points: {points}')

        print(f'{player_name}, do you want to take a new card? [y]es/[n]o')
        answer = input().lower()
        if self.read_quit(answer):
            return

        if answer in ('y', 'yes'):
            self.out_msg.send(ProtocolCommand.TAKE_CARD, {'take_card': True})
        elif answer in ('n', 'no'):
            self.out_msg.send(ProtocolCommand.TAKE_CARD, {'take_card': False})
            print('Wait until round ends')
        else:
            print('Unknown input. Please repeat')
            self.start_round(round, points, player_name)

    def receive_card(self, suit, rank, points):
        card = Card(suit, rank)
        print(front_card(card))
        print(f"Your points: {points}")

    def show_choice_notification(self, player_name):
        print(f'{player_name} made a choice')

    def you_win(self):
        print('You are winner!')

    def someone_wins(self, player_name, points):
        print(f'{player_name} wins! Points: {points}')

    def you_lose(self):
        print('You lose')

    def someone_loses(self, player_name, points):
        print(f'{player_name} loses. Points: {points}')

    def game_over(self):
        menu_print('Game over')
        self.read_quit(input())

    def read_quit(self, input):
        if input in ('stop', 'quit', 'exit'):
            self.close()
            return True
        return False

    def close(self):
        print("closing connection to", self.addr)
        self.selector.unregister(self.sock)
        self.sock.close()
