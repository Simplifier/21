import random
from itertools import product

from cards import Card

suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

deck = list(product(suits, cards))


def get_random_card():
    if len(deck) == 0:
        return None

    card = random.choice(deck)
    deck.remove(card)
    return Card(*card)
