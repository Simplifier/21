from client_deck import random_card
from client_cards import *
import client_menu
import datetime
from _server_settings import *
from time import sleep


class Player():

    def __init__(self, name, addr):

        self.name = name
        self.addr = addr
        self.points = 0
        self.state = True
        self.cards = []
        self.game = 0
        self.req = False
        self.messages = {}
        self.isAdmin = False


    def update(self):

        if self.points > 21:
            self.state = False
            self.loose()

    def request(self):

        self.send(client_menu.line('#', 50))
        self.send('|###' + self.name + '  ' + 'Points: ' + str(self.points)  )
        self.t = self.send(self.name + ", do you want to take a new card? [Y(Enter)/N]")
        self.answ = False

        while not self.answ:

            if len(self.messages) !=0:

                #try:
                    self.data = self.messages.pop(self.t, "None")
                    print(f"[{self.name} message]", self.data)
                    print(self.messages)
                    if self.data.upper() in ['Y', 'YES', '']:
                        self.get_card()
                        self.send("You points: " + str(self.points))
                    else:
                        self.state = False
                        print(self.name, "left round")
                    self.answ = True
                # except:
                #     self.send("It looks like some ERROR...What did you do?")
        self.game.answer(self)




    def get_card(self):
        self.card_suit, self.card_rank = random_card()  # Выбираем случайную карту
        self.card = Card(self.card_suit, self.card_rank)  # Создаем объект карты
        self.cards.append(self.card)  # Добавляем карту в список карт игрока

        self.send(front_card(self.card))
        self.points += self.card.points

    def loose(self):
        self.send(client_menu.doom.renderText("You loose"))

    def send(self, message):

        self.t = str(datetime.datetime.now().timestamp())
        self.message = self.t + '%%' + message
        sock.sendto(self.message.encode("utf-8"), self.addr)
        return self.t

