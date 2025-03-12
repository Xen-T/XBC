import random
import sys
print(sys.path)
import pygame
import pygame.font
import pygame, sys


from PIL import Image, ImageDraw, ImageFont  # For generating card images
 


#this defines our cards and their values in the game
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'J': 10, 'Q': 10, 'K': 10, 'A': 11}
pygame.font.init()
font = pygame.font.Font(None, 36)
pygame.init()

#lines 15-36 is all appearance stuffs for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)





pygame.display.update()


CARD_WIDTH = 80
CARD_HEIGHT = 120


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

#we had an llm help us with the card design, this is for generating the card image
def generate_card_images():
    from PIL import Image, ImageDraw, ImageFont

    
    import os
    if not os.path.exists("cards"):
        os.makedirs("cards")

    
    for rank in ranks:
        for suit in suits:
            
            card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), WHITE)
            draw = ImageDraw.Draw(card)

            
            text = f"{rank}\n{suit[0]}"  
            draw.text((10, 10), text, fill=BLACK, font=ImageFont.load_default())

            
            card_name = f"{rank}_of_{suit.lower()}.png"
            card.save(f"cards/{card_name}")

    
    card_back = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), GREEN)
    draw = ImageDraw.Draw(card_back)
    draw.rectangle([10, 10, CARD_WIDTH - 10, CARD_HEIGHT - 10], outline=WHITE, width=2)
    card_back.save("cards/back_of_back.png")

    print("Card images generated successfully!")


try:
    card_images = {}
    for suit in suits:
        for rank in ranks:
            card_name = f"{rank}_of_{suit.lower()}.png"
            card_images[(rank, suit)] = pygame.image.load(f"cards/{card_name}")
    card_images[('back', 'back')] = pygame.image.load("cards/back_of_back.png")
except FileNotFoundError:
    print("Card images not found. Generating them now...")
    generate_card_images()

    card_images = {}
    for suit in suits:
        for rank in ranks:
            card_name = f"{rank}_of_{suit.lower()}.png"
            card_images[(rank, suit)] = pygame.image.load(f"cards/{card_name}")
    card_images[('back', 'back')] = pygame.image.load("cards/back_of_back.png")

#the class function creates objects and the init initializes objects with values
#so 91-109 is creating objects with different attributes and behaviors for card, deck, hand
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


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

#129-144 is more about drawing text on the screen and draw_cards is drawing from the hand onto the screen
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_cards(hand, x, y, hide_first_card=False):
    for i, card in enumerate(hand.cards):
        if hide_first_card and i == 0:
            screen.blit(card_images[('back', 'back')], (x + i * (CARD_WIDTH + 10), y))
        else:
            screen.blit(card_images[(card.rank, card.suit)], (x + i * (CARD_WIDTH + 10), y))


def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, x + 10, y + 10, BLACK)

#this starts the game, the player and the dealer both recieve their initial cards with lines 151-159
def play_blackjack():
    print("Welcome to Blackjack!")


    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()


    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())


    running = True
    player_turn = True
    game_over = False
#this is for the green board and rendering the messages on the screen; draw_text and draw_cards for when the player takes actions
    while running:
        screen.fill(GREEN)


        draw_text("Your hand:", 50, 50)
        draw_cards(player_hand, 50, 100)


        draw_text("Dealer's hand:", 50, 300)
        if player_turn and not game_over:
            draw_cards(dealer_hand, 50, 350, hide_first_card=True)
        else:
            draw_cards(dealer_hand, 50, 350)


        draw_text(f"Your hand value: {player_hand.hand_value()}", 50, 250)
        if not player_turn or game_over:
            draw_text(f"Dealer's hand value: {dealer_hand.hand_value()}", 50, 500)
#draw_button and player_turn is when the player can choose to draw a card or stand if they have not lost yet.

        if player_turn and not game_over:
            draw_button("Hit", 600, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE)
            draw_button("Stand", 600, 200, BUTTON_WIDTH, BUTTON_HEIGHT, RED)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if player_turn and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if 600 <= mouse_x <= 600 + BUTTON_WIDTH and 100 <= mouse_y <= 100 + BUTTON_HEIGHT:
                        player_hand.add_card(deck.deal_card())
                        if player_hand.hand_value() > 21:
                            player_turn = False
                            game_over = True

                    elif 600 <= mouse_x <= 600 + BUTTON_WIDTH and 200 <= mouse_y <= 200 + BUTTON_HEIGHT:
                        player_turn = False
#211 is a loop that essentially makes it so as long as the dealer has a value <17, they will draw cards until they get 17 or above

        if not player_turn and not game_over:
            while dealer_hand.hand_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            game_over = True

#the following code has a bunch of if, then statements regarding winning or losing the game
#the cards value that is defined gets calculated, and if it is over 21, text is rendered saying we lost
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

        pygame.display.flip()

if __name__ == '__main__':
    play_blackjack()
