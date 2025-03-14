import pygame
import sys
from blackjackcheckpoint8 import *

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack - Home Screen")


TABLE_GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Fonts
title_font = pygame.font.SysFont("Comic Sans MS", 72)
button_font = pygame.font.Font(None, 36)

# Title
title_text = title_font.render("Welcome to Blackjack", True, RED)
title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

# Start Button
button_width, button_height = 200, 50
button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)

# Quit Button
quit_button_width, quit_button_height = 200, 50
quit_button_rect = pygame.Rect(WIDTH // 2 - quit_button_width // 2, HEIGHT // 2 + 100, quit_button_width, quit_button_height)

def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect)
    button_text = button_font.render(text, True, BLACK)
    button_text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, button_text_rect)

def home_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    start_game()
                    return
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(TABLE_GREEN)
        screen.blit(title_text, title_rect)
        draw_button(screen, button_rect, GREEN, "Start Game")
        draw_button(screen, quit_button_rect, RED, "Quit")
        pygame.display.flip()

def start_game():
    play_blackjack() 
    print("Blackjack Game Started!")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((20, 20, 20))  # Example game screen
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    home_screen()