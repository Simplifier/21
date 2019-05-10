from enum import Enum, unique


@unique
class ProtocolCommand(Enum):
    SEND_NAME = 0
    NEW_ROOM = 1
    JOIN_ROOM = 2
    SEND_PASS = 3
    START_GAME = 4
    TAKE_CARD = 5

    PASS_CREATED = 6
    WAIT_PASS = 7
    REJECT_JOIN = 8
    ACCEPT_JOIN = 9
    PLAYER_JOINED = 10
    GAME_CAN_BEGIN = 11
    ROUND_STARTED = 12
    CARD_TAKEN = 13
    PLAYER_TURNED = 14
    YOU_WIN = 15
    PLAYER_WINS = 16
    YOU_LOSE = 17
    PLAYER_LOSES = 18
    GAME_OVER = 19
