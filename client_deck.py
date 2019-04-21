import random
from itertools import product

suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

deck = list(product(suits_name, cards))


def random_card():
    if len(deck) > 0:
        card = random.choice(deck)
        deck.remove(card)
        return card
    else:
        return False
