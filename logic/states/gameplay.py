import pygame, random
from logic.states.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, DEALER_CARD_DELAY, MAX_THROWN_CARD_VELOCITY, DEALED_CARD_POSSIBLE_Y_OFFSET

gameplay_background = None
thrown_card_min_height = thrown_card_max_height = None
stand_button_text = stand_button_rect = None
hit_button_text = hit_button_rect = None
player_bust = dealer_bust = stand = False
dealer_points = player_points = dealer_card_delay = 0


def init_gameplay_state(game):
    global gameplay_background, \
           thrown_card_min_height, thrown_card_max_height, \
           stand_button_text, stand_button_rect, \
           hit_button_text, hit_button_rect

    gameplay_background = game.generic_background.copy()
    thrown_card_min_height = (SCREEN_HEIGHT // 2) - DEALED_CARD_POSSIBLE_Y_OFFSET
    thrown_card_max_height = (SCREEN_HEIGHT // 2) + DEALED_CARD_POSSIBLE_Y_OFFSET
    stand_button_text = game.gameplay_buttons_font.render("Stand", True, 'black')
    stand_button_rect = stand_button_text.get_rect(center = (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT // 2))
    hit_button_text = game.gameplay_buttons_font.render("Hit", True, 'black')
    hit_button_rect = hit_button_text.get_rect(center = (SCREEN_WIDTH * 0.9, SCREEN_HEIGHT // 2))

def handle_gameplay_events(game, event):
    global player_bust, stand

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e and len(game.dealer_cards) == 0:
            cards_to_remove = []
            card_added = False #Boolean to keep track if card is added or not (and to stop the code from updating the player hand rects if no card is added)
            for card in game.thrown_cards:
                if card.owner == 'player':
                    card_added = True
                    card.flip() #Flip the card so that it is visible in the player's hand
                    card.reset_rotation() #Reset the card's rotation to its original rotation
                    card.reset_surf_size() #Reset the card's size to its original size (rotating the card can modify the size of the card)
                    game.player_hand.append(card)
                    cards_to_remove.append(card)
            [game.thrown_cards.remove(element) for element in cards_to_remove]
            if card_added: game.update_player_hand_rects()  # Update the rects for the player's hand

            if len(game.dealer_cards) == 0: game.add_cards_to_dealer(2) #Place the two initial cards of the dealer

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hit_button_rect.collidepoint(event.pos) and len(game.player_hand) != 0:
            add_card_to_player_hand(game)
            
        elif stand_button_rect.collidepoint(event.pos) and len(game.player_hand) != 0:
            stand = True

    elif event.type == pygame.MOUSEMOTION:
        if len(game.player_hand) != 0: 
            raise_card_in_hand(game, event.pos)

def update_gameplay_logic(game):
    global stand, player_bust, dealer_bust, dealer_card_delay

    # Animate thrown cards
    min_height = thrown_card_min_height
    max_height = thrown_card_max_height
    for card in game.thrown_cards:
        velocity = calculate_velocity(card.rect.centery)
        if not min_height <= card.rect.centery <= max_height:
            card.rect.centery += velocity  # Move the card down
        elif card.owner == 'dealer':
            game.dealer_cards.append(card)
            game.thrown_cards.remove(card)

    #Check for player player_bust
    if not player_bust:
        player_points = 0
        for card in game.player_hand:
            player_points += card.value
            if player_points > 21:
                player_bust = True
                break

    if stand:
        dealer_points = 0
        if dealer_points < 17:
            if dealer_card_delay >= DEALER_CARD_DELAY:
                game.add_cards_to_dealer(1)
                dealer_card_delay = 0  # Reset the delay counter
            else:
                dealer_card_delay += 1  # Increment the delay counter

            for card in game.dealer_cards:
                dealer_points += card.value
                if dealer_points > 21:
                    dealer_bust = True
                    stand = False
                    break

def render_gameplay(game):
    game.fake_screen.blit(gameplay_background, (0, 0))

    #Draw thrown cards
    [card.draw(game.fake_screen) for card in game.thrown_cards]
    #Draw player hand
    [card.draw(game.fake_screen) for card in game.player_hand]
    #Draw dealer cards
    [card.draw(game.fake_screen) for card in game.dealer_cards]
    #Draw buttons
    game.fake_screen.blit(stand_button_text, stand_button_rect)
    game.fake_screen.blit(hit_button_text, hit_button_rect)

def raise_card_in_hand(game, pos):
    raised_card_max_height = game.cards_in_hand_y_value - (game.card_height * 0.3)
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

def add_card_to_player_hand(game):
    card = random.choice(game.deck)
    card.set_owner('player')
    game.deck.remove(card)
    game.player_hand.append(card)
    game.update_player_hand_rects()