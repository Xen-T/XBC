import random
import sys
import pygame
import pygame.font

# Initialize Pygame
pygame.init()
pygame.font.init()

# Load and play background music
pygame.mixer.music.load("XBC/funjazz.mp3")
pygame.mixer.music.play(-1, 0.0)  # Play the music indefinitely

# Define card ranks, suits, and values
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Card dimensions
CARD_WIDTH = 80
CARD_HEIGHT = 120

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Font for text
font = pygame.font.Font(None, 36)

# Load custom card images and resize them
card_images = {}
for suit in suits:
    for rank in ranks:
        card_name = f"XBC/cards/{rank}_of_{suit.lower()}.png"  # Updated path
        try:
            image = pygame.image.load(card_name)
            card_images[(rank, suit)] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        except FileNotFoundError:
            print(f"Error: File {card_name} not found. Please check the file path and name.")
            sys.exit()

# Load and resize the back of the card image
try:
    back_image = pygame.image.load("XBC/cards/back_of_card.png")  # Updated path
    card_images[('back', 'back')] = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
except FileNotFoundError:
    print("Error: File XBC/cards/back_of_card.png not found. Please check the file path and name.")
    sys.exit()

# Card class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

# Hand class
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

# Function to draw text on the screen
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw cards on the screen
def draw_cards(hand, x, y, hide_first_card=False):
    for i, card in enumerate(hand.cards):
        if hide_first_card and i == 0:
            screen.blit(card_images[('back', 'back')], (x + i * (CARD_WIDTH + 10), y))
        else:
            screen.blit(card_images[(card.rank, card.suit)], (x + i * (CARD_WIDTH + 10), y))

# Function to draw buttons on the screen
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, x + 10, y + 10, BLACK)

# Main game function
def play_blackjack():
    print("Welcome to Blackjack!")

    # Initialize deck and hands
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    # Deal initial cards
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Game state variables
    running = True
    player_turn = True
    game_over = False

    # Main game loop
    while running:
        screen.fill(GREEN)

        # Draw player's hand
        draw_text("Your hand:", 50, 50)
        draw_cards(player_hand, 50, 100)

        # Draw dealer's hand
        draw_text("Dealer's hand:", 50, 300)
        if player_turn and not game_over:
            draw_cards(dealer_hand, 50, 350, hide_first_card=True)
        else:
            draw_cards(dealer_hand, 50, 350)

        # Display hand values
        draw_text(f"Your hand value: {player_hand.hand_value()}", 50, 250)
        if not player_turn or game_over:
            draw_text(f"Dealer's hand value: {dealer_hand.hand_value()}", 50, 500)

        # Draw buttons during player's turn
        if player_turn and not game_over:
            draw_button("Hit", 600, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE)
            draw_button("Stand", 600, 200, BUTTON_WIDTH, BUTTON_HEIGHT, RED)

        # Draw "Play Again" button when the game is over
        if game_over:
            draw_button("Play Again", 600, 300, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if player_turn and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Hit button
                    if 600 <= mouse_x <= 600 + BUTTON_WIDTH and 100 <= mouse_y <= 100 + BUTTON_HEIGHT:
                        player_hand.add_card(deck.deal_card())
                        if player_hand.hand_value() > 21:
                            player_turn = False
                            game_over = True

                    # Stand button
                    elif 600 <= mouse_x <= 600 + BUTTON_WIDTH and 200 <= mouse_y <= 200 + BUTTON_HEIGHT:
                        player_turn = False

            # "Play Again" button
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 600 <= mouse_x <= 600 + BUTTON_WIDTH and 300 <= mouse_y <= 300 + BUTTON_HEIGHT:
                    # Reset the game state
                    deck = Deck()
                    player_hand = Hand()
                    dealer_hand = Hand()

                    # Deal initial cards
                    player_hand.add_card(deck.deal_card())
                    dealer_hand.add_card(deck.deal_card())
                    player_hand.add_card(deck.deal_card())
                    dealer_hand.add_card(deck.deal_card())

                    # Reset game flags
                    player_turn = True
                    game_over = False

        # Dealer's turn
        if not player_turn and not game_over:
            while dealer_hand.hand_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            game_over = True

        # Determine game outcome
        if game_over:
            player_value = player_hand.hand_value()
            dealer_value = dealer_hand.hand_value()

            if player_value > 21:
                draw_text("You busted! Dealer wins.", 50, 550)
            elif dealer_value > 21:
                draw_text("Dealer busted! You win!", 50, 550)
            elif player_value > dealer_value:
                draw_text("You win!", 50, 550)
            elif dealer_value > player_value:
                draw_text("Dealer wins!", 50, 550)
            else:
                draw_text("It's a tie!", 50, 550)

        # Update the display
        pygame.display.flip()

# Run the game
if __name__ == '__main__':
    play_blackjack()