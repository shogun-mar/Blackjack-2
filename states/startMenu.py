import pygame
from states.gameState import GameState
from random import sample
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

#Variables
play_message_resize_factor = 1
play_message_resize_amount = 0.01

def handle_start_menu_events(game, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            add_random_cards_to_player_hand(game)
            game.game_state = GameState.GAMEPLAY
    
def update_start_menu_logic(game):
    global play_message_resize_factor

    # Resize play message
    play_message_resize_factor += play_message_resize_amount
    if play_message_resize_factor > 2:
        play_message_resize_factor = 1

    original_width, original_height = game.play_message_original_size
    new_width = int(original_width * play_message_resize_factor)
    new_height = int(original_height * play_message_resize_factor)
    game.play_message = pygame.transform.scale(game.play_message_original, (new_width, new_height))
    game.play_message_rect.size = game.play_message.get_size()
    game.play_message_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)

def render_start_menu(game):
    game.fake_screen.blit(game.background, (0, 0))
    game.fake_screen.blit(game.play_message, game.play_message_rect)

def add_random_cards_to_player_hand(game):
    #Sample return a list of 2 unique random elements from the cards_dict
    random_keys = sample(list(game.cards_dict.keys()), 2)
    for key in random_keys:
        game.player_hand.append(game.cards_dict[key])