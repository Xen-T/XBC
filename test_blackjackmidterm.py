import unittest
import random

# Import the classes and functions from your game code
from blackjackmidterm import Card, Deck, Hand, values  # Replace 'your_game_file' with the name of your Python file

class TestBlackjack(unittest.TestCase):
    def test_card_creation(self):
        """Test if a Card object is created correctly."""
        card = Card("A", "Hearts")
        self.assertEqual(card.rank, "A")
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(str(card), "A of Hearts")

    def test_deck_creation(self):
        """Test if a Deck object is created correctly and contains 52 cards."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_shuffle(self):
        """Test if the deck is shuffled."""
        deck1 = Deck()
        deck2 = Deck()
        self.assertNotEqual(deck1.cards, deck2.cards)  # Shuffled decks should not be the same

    def test_deck_deal_card(self):
        """Test if a card is dealt correctly from the deck."""
        deck = Deck()
        initial_count = len(deck.cards)
        card = deck.deal_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), initial_count - 1)

    def test_hand_add_card(self):
        """Test if a card is added to a hand correctly."""
        hand = Hand()
        card = Card("K", "Spades")
        hand.add_card(card)
        self.assertEqual(len(hand.cards), 1)
        self.assertEqual(str(hand.cards[0]), "K of Spades")

    def test_hand_value_no_aces(self):
        """Test the hand value calculation without aces."""
        hand = Hand()
        hand.add_card(Card("7", "Diamonds"))
        hand.add_card(Card("Q", "Hearts"))
        self.assertEqual(hand.hand_value(), 17)

    def test_hand_value_with_aces(self):
        """Test the hand value calculation with aces."""
        hand = Hand()
        hand.add_card(Card("A", "Spades"))
        hand.add_card(Card("9", "Clubs"))
        self.assertEqual(hand.hand_value(), 20)  # Ace counts as 11

        hand.add_card(Card("5", "Diamonds"))
        self.assertEqual(hand.hand_value(), 15)  # Ace counts as 1 after going over 21

    def test_hand_value_multiple_aces(self):
        """Test the hand value calculation with multiple aces."""
        hand = Hand()
        hand.add_card(Card("A", "Hearts"))
        hand.add_card(Card("A", "Diamonds"))
        hand.add_card(Card("A", "Clubs"))
        self.assertEqual(hand.hand_value(), 13)  # Two aces count as 1, one as 11

    def test_hand_value_bust(self):
        """Test if the hand value correctly identifies a bust."""
        hand = Hand()
        hand.add_card(Card("10", "Spades"))
        hand.add_card(Card("J", "Hearts"))
        hand.add_card(Card("2", "Diamonds"))
        self.assertEqual(hand.hand_value(), 22)  # Bust

    def test_hand_str_representation(self):
        """Test the string representation of a hand."""
        hand = Hand()
        hand.add_card(Card("4", "Clubs"))
        hand.add_card(Card("K", "Diamonds"))
        self.assertEqual(str(hand), "4 of Clubs, K of Diamonds")

# Run the tests
if __name__ == "__main__":
    unittest.main()