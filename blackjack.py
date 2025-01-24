git config user.email "ceswope"
  git config --global user.name "Your Name"

import random

# Define card ranks and suits
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Card class to represent each card
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Deck class to manage a deck of cards
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

# Hand class to manage the player's or dealer's hand
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def hand_value(self):
        value = sum(values[card.rank] for card in self.cards)
        ace_count = sum(1 for card in self.cards if card.rank == 'A')

        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

# Function to play Blackjack
def play_blackjack():
    print("Welcome to Blackjack!")

    # Initialize deck, player's hand, and dealer's hand
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    # Deal initial cards
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Show hands
    print("\nYour hand:", player_hand)
    print("Dealer's hand: ", dealer_hand.cards[0], "and an unknown card.")

    # Player's turn
    while player_hand.hand_value() < 21:
        choice = input("\nDo you want to 'hit' or 'stand'? ").lower()
        if choice == 'hit':
            player_hand.add_card(deck.deal_card())
            print("\nYour hand:", player_hand)
        elif choice == 'stand':
            break

    # Dealer's turn
    if player_hand.hand_value() <= 21:
        print("\nDealer's hand:", dealer_hand)
        while dealer_hand.hand_value() < 17:
            print("Dealer hits.")
            dealer_hand.add_card(deck.deal_card())
            print("Dealer's hand:", dealer_hand)

    # Determine winner
    player_value = player_hand.hand_value()
    dealer_value = dealer_hand.hand_value()

    print(f"\nYour hand value: {player_value}")
    print(f"Dealer's hand value: {dealer_value}")

    if player_value > 21:
        print("You busted! Dealer wins.")
    elif dealer_value > 21:
        print("Dealer busted! You win!")
    elif player_value > dealer_value:
        print("You win!")
    elif dealer_value > player_value:
        print("Dealer wins!")
    else:
        print("It's a tie!")

if __name__ == '__main__':
    play_blackjack()
