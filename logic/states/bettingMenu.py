import pygame
from logic.states.gameState import GameState
from settings import MENU_BACKGROUNDS_ALPHA_VALUE, SCREEN_WIDTH, SCREEN_HEIGHT

current_bet = 0
betting_menu_static_ui_surfs = None
betting_menu_static_ui_rects = None
betting_menu_interactible_ui_surfs = []
betting_menu_interactible_ui_rects = []
current_bet_text = None
current_bet_text_rect = None
betting_menu_background = None
num_static_ui_elements = None
num_interactible_ui_elements = None
betting_menu_white_panel_rect = None
betting_menu_black_panel_rect = None
can_start_game = None

def init_betting_menu(game):
    global betting_menu_static_ui_surfs, betting_menu_static_ui_rects, \
           current_bet_text, current_bet_text_rect, betting_menu_background, \
           num_static_ui_elements, betting_menu_white_panel_rect, \
           betting_menu_black_panel_rect, num_interactible_ui_elements

    panel_surf_size = (800, 300)
    betting_menu_background = game.generic_background.copy() #Darkened background
    darken_surf = pygame.Surface(betting_menu_background.get_size(), pygame.SRCALPHA) # SRCALPHA flag do have per pixel transparency
    darken_surf.fill((0, 0, 0, MENU_BACKGROUNDS_ALPHA_VALUE)) #Fill it with half transparent black
    betting_menu_background.blit(darken_surf, (0, 0)) #Blit the half dark surf on the background

    #Panels
    betting_menu_black_panel = pygame.Surface(panel_surf_size)
    betting_menu_black_panel_rect = betting_menu_black_panel.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    betting_menu_white_panel = pygame.Surface(panel_surf_size)
    betting_menu_white_panel.fill('white')
    betting_menu_white_panel_rect = betting_menu_white_panel.get_rect(center = (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 20))

    #Texts
    player_money_text = game.betting_message_font.render(f"Your current balance: {game.player_money} $", 'black', True) 
    player_money_text_rect = player_money_text.get_rect(center = (SCREEN_WIDTH // 2, betting_menu_white_panel_rect.midtop[1] + betting_menu_black_panel_rect.height * 0.2))
    current_bet_text = game.betting_message_font.render("Current bet: 0", 'black', True)
    current_bet_text_rect = current_bet_text.get_rect(center = (SCREEN_WIDTH // 2, betting_menu_white_panel_rect.midbottom[1] - betting_menu_black_panel_rect.height * 0.2))

    #Static ui elements
    betting_menu_static_ui_surfs = [betting_menu_black_panel, betting_menu_white_panel, player_money_text, current_bet_text]
    betting_menu_static_ui_rects = [betting_menu_black_panel_rect, betting_menu_white_panel_rect, player_money_text_rect, current_bet_text_rect]
    
    #Interactible ui elements
    options = [("10", 0.25), ("25", 0.5), ("50", 0.75)]
    for text, pos_factor in options:
        option_surf = game.betting_options_font.render(text, True, 'black')
        option_rect = option_surf.get_rect(center=(betting_menu_white_panel_rect.midleft[0] + betting_menu_white_panel_rect.width * pos_factor, betting_menu_white_panel_rect.centery))
        betting_menu_interactible_ui_surfs.append(option_surf)
        betting_menu_interactible_ui_rects.append(option_rect)
    
    play_button_text = game.betting_options_font.render("Press E to start", True, 'grey')
    play_button_text_rect = play_button_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8))
    betting_menu_interactible_ui_surfs.append(play_button_text)
    betting_menu_interactible_ui_rects.append(play_button_text_rect)

    num_static_ui_elements = len(betting_menu_static_ui_surfs)
    num_interactible_ui_elements = len(betting_menu_interactible_ui_surfs)

def handle_betting_menu_events(game, event):
    global current_bet, can_start_game

    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
        if can_start_game:
            game.deal_cards_to_player(2)
            game.game_state = GameState.GAMEPLAY

    elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3): #Left or right click
        betting_values = [10, 25, 50]
        for i in range(len(betting_values)):
            if betting_menu_interactible_ui_rects[i].collidepoint(event.pos):
                if i < len(betting_values) and current_bet + betting_values[i] <= game.player_money:
                    current_bet += betting_values[i]
                    break

        #Update current bet surf and rect (the last element in the list)
        betting_menu_static_ui_surfs[-1] = game.betting_message_font.render(f"Current bet: {current_bet}", True, 'black')
        betting_menu_static_ui_rects[-1].center = (SCREEN_WIDTH // 2, betting_menu_white_panel_rect.midbottom[1] - betting_menu_black_panel_rect.height * 0.2)
        #Update the play button
        betting_menu_interactible_ui_surfs[-1] = game.betting_options_font.render("Press E to start", True, 'black')
        can_start_game = True

def update_betting_menu_logic():
    ...

def render_betting_menu(game):
    #Draw background
    game.fake_screen.blit(betting_menu_background, (0, 0))
    #Draw UI
    [game.fake_screen.blit(betting_menu_static_ui_surfs[i], betting_menu_static_ui_rects[i]) for i in range(num_static_ui_elements)]
    [game.fake_screen.blit(betting_menu_interactible_ui_surfs[i], betting_menu_interactible_ui_rects[i]) for i in range(num_interactible_ui_elements)]