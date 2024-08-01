import pygame
from logic.states.gameState import GameState

def handle_betting_menu_events(game, event):
    ...

def update_betting_menu_logic():
    ...

def render_betting_menu(game):
    #Draw background
    game.fake_screen.blit(game.betting_menu_background, (0, 0))
    #Draw UI
    [game.fake_screen.blit(game.betting_static_menu_ui[i], game.betting_menu_static_ui_rects[i]) for i in range(len(game.betting_static_+menu_ui))]