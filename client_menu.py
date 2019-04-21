
import pyfiglet

banner = pyfiglet.Figlet(font='banner3')
doom = pyfiglet.Figlet(font='doom')
cat = pyfiglet.Figlet(font ='catwalk')


def start_message():
    print("""
    Hello! Welcome to 21! 
    If player have over 21 point - player loose
    If player have  21 point - player win
    If no one scored 21 points, the one who was closest wins.\n""")

def show_players(players):
    print()
    print(line('_', 50))
    print(doom.renderText('PLAYERS'))
    for player in players:
        #print(doom.renderText((player.name + " : " + str(player.points))))
        print('###   '+player.name, ':', player.points)

    print(line('_', 50))


def line(sym, l):
    return ''.join([sym for i in range(l)])


def menuprint(text):
    print(banner.renderText(text))
