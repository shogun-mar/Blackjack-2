import pygame
from logic.states.gameState import GameState

def handle_gameplay_events(game, event):
    if event.type == pygame.KEYDOWN:
        ...
    elif event.type == pygame.MOUSEBUTTONDOWN:
        ...
    elif event.type == pygame.MOUSEMOTION:
        

def update_gameplay_logic():
    ...

def render_gameplay(game):
    game.fake_screen.blit(game.background, (0, 0))
    for card in game.player_hand:
        game.fake_screen.blit(card.sprite, card.rect)