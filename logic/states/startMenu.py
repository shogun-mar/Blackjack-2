import pygame
from logic.states.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

#Variables
play_message_resize_factor = 1
play_message_resize_amount = 0.01

def handle_start_menu_events(game, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            game.deal_cards_to_player(2)
            game.game_state = GameState.GAMEPLAY
    
def update_start_menu_logic(game):
    global play_message_resize_factor, play_message_resize_amount
    
    # Update resize factor
    if play_message_resize_factor >= 2 or play_message_resize_factor <= 1:
        play_message_resize_amount *= -1
    play_message_resize_factor = max(1, play_message_resize_factor + play_message_resize_amount)

    # Resize play message
    game.play_message_outline, game.play_message_outline_rect.size = resize_surface(
        game.play_message_original, game.play_message_original_size, play_message_resize_factor
    )

    game.play_message_outline_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

def render_start_menu(game):
    game.fake_screen.blit(game.background, (0, 0))
    game.fake_screen.blit(game.play_message_outline, game.play_message_outline_rect)
    #game.fake_screen.blit(game.play_message, game.play_message_rect)

def resize_surface(surface, original_size, resize_factor):
    original_width, original_height = original_size
    new_width = int(original_width * resize_factor)
    new_height = int(original_height * resize_factor)
    resized_surface = pygame.transform.scale(surface, (new_width, new_height))
    return resized_surface, resized_surface.get_size()



