import pygame
from states.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

#Variables
play_message_resize_factor = 1
play_message_resize_amount = 0.02

def handle_start_menu_events(event):
    if event == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return GameState.GAMEPLAY
    
def update_start_menu_logic(game):
    #Resize play message
    play_message_resize_factor += play_message_resize_amount
    if play_message_resize_factor > 2: play_message_resize_factor = 1
    play_message = pygame.transform.scale(play_message, (int(game.play_message_original_size[0] * play_message_resize_factor), int(game.play_message_original_size[1] * play_message_resize_factor)))
    #play_message_rect = play_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

def render_start_menu(game):
    game.fake_screen.blit(game.background, (0, 0))
    game.fake_screen.blit(game.play_message, game.play_message_rect)