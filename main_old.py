from client_menu import *
from _classPlayer import *
from time import sleep

def make_players():
    players = []
    exit = False
    while not exit:
        name = input("Enter your name, please [Name/exit, e, enter]: ")
        if name.lower() not in ['exit', 'e', '', 'enter']:
            players.append(Player(name))
        else:
            exit = True
    return players



start_message()
players = make_players()
show_players(players)

round = 1
game = True
while game:
    game = False

    menuprint("ROUND "+str(round))

    for name in players:
        if name.state:
            name.update()
            game = game or name.state
            sleep(1)
    round += 1

#################################################################
sleep(1)
menuprint('end')
sleep(1)
show_players(players)

winner = "Nobody"
win_points = 0

for player in players:
    if win_points <= player.points <= 21:
        win_points = player.points
        winner = player.name
sleep(1)
menuprint(winner + " win !")
