import threading
from random import randint
from time import sleep

from _classGame import *
from _classPlayer import *

games = {}  # все игры
players = {}

def server_commands():
    command = input()
    if command.upper() == "STOP":
        quit = True


# NEW PLAYER
def new_player(player, sock):
    t = player.send('Do you want to start NEW game or JOIN an existing game?[NEW/JOIN]\n')
    add = False
    while not add:
        if len(player.messages) > 0:

            data = player.messages.pop(t, "None")

            # НОВАЯ ИГРА
            if data.upper() in ['NEW', 'N']:

                if new_game(player):
                    add = True


            # ПРИСОЕДИНИТЬСЯ К ТЕКУЩЕЙ ИГРЕ
            elif data.upper() in ['JOIN', 'J']:

                if join_game(player):
                    add = True


# Создаём новую игру, назначаем игрока админом и отправляем пароль
def new_game(player):
    passw = randint(1000, 10000)
    game = Game(player, passw)
    games[passw] = game
    player.isAdmin = True
    player.game = game
    message = 'your pass: ' + str(passw) + '\n'
    player.send(message + '\ntype [start] when you are ready')
    print("[SERVER]", player.name, "start new game")
    return True

# Игрок хочет присоединиться к игре
def join_game(player):
    t = player.send('Enter pass game: ')
    add = False
    while not add:
        if len(player.messages) > 0:

            data = player.messages.pop(t, "None")

            try:
                data = int(data)
                game = games[data]
                player.game = game
                game.players.append(player)
                player.send('You have successfully connected to the game.')
                game.admin.send("New player connected: " + player.name)
                add = True
                print("[SERVER]", player.name, "join game", game.admin.name )

            except Exception as e:
                t = player.send('No such game. Try again: ')

    return True

# NEW PLAYER END

def main_game(name, game):

    while game.state:
        if not game.round_state:
            game.start_round()

    game.send("GAME END")
    winner = "Nobody"
    win_points = 0

    for player in game.players:
        if win_points <= player.points <= 21:
            win_points = player.points
            winner = player.name
    sleep(1)
    game.send(winner + " win !")


quit = False

commandT = threading.Thread(target=server_commands, args=())
commandT.start()
while not quit:
    #try:
        data, addr = sock.recvfrom(1024)
        data = data.decode("utf-8")
        t, data = data.split('%%')


        print("Addr: ", *addr, "data: ", data, "t:", t)

        # НОВЫЙ ЮЗЕР
        if   t== '0' or addr not in players.keys():
            if t == '0':

                name = data
                player = Player(data, addr)
                players[addr] = player

                playerT = threading.Thread(target=new_player, args=(player, sock))
                playerT.start()


        # ЮЗЕР СУЩЕСТВУЕТ
        else:

            player = players[addr]

            if t == '1':
                pass
            if t == '2':
                pass



            if t == '3':

                #Если игра не запущена и игрок является админом игры
                if player.game.state == False and player.game.admin.addr == addr:
                    player.game.state = True
                    player.game.send("BEGIN GAME")

                    gameT = threading.Thread(target=main_game, args=("boo", player.game))
                    gameT.start()
            else:
                player.messages[t] = data
    # except:
    #     quit = True

for game in games.values():
    game.send("[Server stopped]")
print(["Server stopped"])
sock.close()
