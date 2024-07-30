import pygame
from logic.states.gameState import GameState
from settings import SCREEN_HEIGHT

def handle_gameplay_events(game, event):
    if event.type == pygame.KEYDOWN:
        ...
    elif event.type == pygame.MOUSEBUTTONDOWN:
        ...
    elif event.type == pygame.MOUSEMOTION:
        if event.pos[1] > SCREEN_HEIGHT - 200: #Non necessary if statement to avoid unnecessary calculations if the mouse if
            raise_card_in_hand(game, event.pos)               # nowhere near the player's hand

def update_gameplay_logic():
    ...

def render_gameplay(game):
    game.fake_screen.blit(game.background, (0, 0))
    for card in game.player_hand:
        game.fake_screen.blit(card.sprite, card.rect)

def raise_card_in_hand(game, pos):
    raised_card_max_height = 620
    raising_amount = 10
    for card in game.player_hand:
        is_mouse_colliding = card.rect.collidepoint(pos)
        if is_mouse_colliding and card.rect.y >= raised_card_max_height:
            if card.rect.y - raising_amount >= raised_card_max_height:
                card.rect.y -= raising_amount
            else:
                card.rect.y = raised_card_max_height
        elif not is_mouse_colliding:
            card.rect.y = game.cards_in_hand_y_value #Reset the card y value
