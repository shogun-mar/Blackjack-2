import pygame
from states.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

#Variables
play_message_resize_factor = 1
play_message_resize_amount = 0.02

#Surfaces
background = pygame.image.load("graphics/background.jpg").convert_alpha()

font = pygame.font.Font("graphics/mx5x7.ttf", 36)
play_message = font.render("Press SPACE to play !", True, (255, 255, 255))
play_message_original_size = play_message.get_size()
play_message_rect = play_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

def handle_start_menu_events(event):
    if event == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return GameState.GAMEPLAY
    
def update_start_menu_logic():
    global play_message_resize_factor

    #Resize play message
    play_message_resize_factor += play_message_resize_amount
    if play_message_resize_factor > 2: play_message_resize_factor = 1
    play_message = pygame.transform.scale(play_message, (int(play_message_original_size[0] * play_message_resize_factor), int(play_message_original_size[1] * play_message_resize_factor)))
    #play_message_rect = play_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

def render_start_menu(screen):
    screen.blit(background, (0, 0))
    screen.blit(play_message, play_message_rect)