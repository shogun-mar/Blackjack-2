import pygame
from logic.states.gameState import GameState
from settings import SCREEN_HEIGHT, DEALED_CARD_POSSIBLE_Y_OFFSET, MAX_THROWN_CARD_VELOCITY

def handle_gameplay_events(game, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e and len(game.cards_on_table) != 0: #Player can only pick up cards if there are cards on the table
            elements_to_remove = []
            for card in game.cards_on_table:
                card.flip() #Flip the card so that it is visible in the player's hand
                card.reset_rotation() #Reset the card's rotation to its original rotation
                card.reset_surf_size() #Reset the card's size to its original size (rotating the card can modify the size of the card)
                game.player_hand.append(card)
                elements_to_remove.append(card)
            [game.cards_on_table.remove(element) for element in elements_to_remove]
            game.update_player_hand_rects()  # Update the rects for the player's hand

    elif event.type == pygame.MOUSEBUTTONDOWN:
        ...
    elif event.type == pygame.MOUSEMOTION:
        if event.pos[1] > SCREEN_HEIGHT - 200 and len(game.player_hand) != 0: #Non necessary if statement to avoid unnecessary calculations if the mouse if
            raise_card_in_hand(game, event.pos)               # nowhere near the player's hand

def update_gameplay_logic(game):
    # Animate thrown cards
    cards_to_be_removed = []
    min_height = (SCREEN_HEIGHT // 2) - DEALED_CARD_POSSIBLE_Y_OFFSET
    max_height = (SCREEN_HEIGHT // 2) + DEALED_CARD_POSSIBLE_Y_OFFSET
    for card in game.animated_cards:
        velocity = calculate_velocity(card.rect.centery)
        if min_height <= card.rect.centery <= max_height:
            game.cards_on_table.append(card)
            cards_to_be_removed.append(card)  # Mark the card for removal from the animated cards list
        else:
            card.rect.centery += velocity  # Move the card down

    for card in cards_to_be_removed:
        game.animated_cards.remove(card)  # Remove the card from the animated cards list

def render_gameplay(game):
    game.fake_screen.blit(game.background, (0, 0))

    #Draw animated cards
    [card.draw(game.fake_screen) for card in game.animated_cards]
    #Draw cards on table
    [card.draw(game.fake_screen) for card in game.cards_on_table]
    #Draw player hand
    #[card.draw(game.fake_screen) for card in game.player_hand]
    for card in game.player_hand:
        #card.front_sprite.fill((255, 255, 255))
        card.draw(game.fake_screen)

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

def calculate_velocity(card_y):
    center_y = SCREEN_HEIGHT // 2
    distance_from_center = abs(card_y - center_y)
    max_distance = center_y  # The maximum distance is from the center to the top or bottom of the screen
    # Calculate velocity as a proportion of the maximum distance
    velocity = (distance_from_center / max_distance) * MAX_THROWN_CARD_VELOCITY
    return velocity
