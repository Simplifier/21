import pyfiglet

banner = pyfiglet.Figlet(font='banner3')
doom = pyfiglet.Figlet(font='doom')
cat = pyfiglet.Figlet(font='catwalk')


def show_rules():
    print("""
    Hello! Welcome to 21! 
    If player has over 21 points - player loses
    If player has 21 points - player wins
    If no one scored 21 points, the one who was the closest wins.\n""")


def menu_print(text):
    print(banner.renderText(text))
