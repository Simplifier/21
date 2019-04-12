from itertools import product
import random
suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

deck = list(product(suits_name, cards))

def random_card():
    card = random.choice(deck)
    deck.remove(card)
    return card


