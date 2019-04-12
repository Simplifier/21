from numbers import show_card
from deck import random_card
from cards import *
import menu


class Player():

    def __init__(self, name):

        self.name = name
        self.points = 0
        self.state = True
        self.cards = []

    def update(self):

        if self.state:
            self.request()
        if self.points > 21:
            self.state = False
            self.loose()

    def request(self):
        print()
        print(menu.line('#', 50))
        print('|###' + self.name + '  ' + 'Points: ' + str(self.points)  )
        #print(menu.doom.renderText(self.name+'  :  '+str(self.points)))
        answ = input(self.name + ", do you want to take a new card? [Y(Enter)/N]\n")
        if answ.upper() in ['Y', 'YES', '']:
            self.get_card()
            print("You points: ", self.points)

        else:
            self.state = False

    def get_card(self):
        card_suit, card_rank = random_card()  # Выбираем случайную карту
        card = Card(card_suit, card_rank)  # Создаем объект карты
        self.cards.append(card)  # Добавляем карту в список карт игрока

        print(front_card(card))
        self.points += card.points

    def loose(self):
        print(menu.doom.renderText("You loose"))