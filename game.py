import pygame, random, os
from logic.states.gameState import GameState
from logic.card import Card
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE, MOUSEMOTION
from logic.states.gameplay import handle_gameplay_events, update_gameplay_logic, render_gameplay, init_gameplay_state
from logic.states.powerupMenu import handle_powerup_menu_events, update_powerup_menu_logic, render_powerup_menu
from logic.states.startMenu import handle_start_menu_events, update_start_menu_logic, render_start_menu, init_start_menu
from logic.states.pauseMenu import handle_pause_menu_events, update_pause_menu_logic, render_pause_menu
from logic.states.bettingMenu import handle_betting_menu_events, update_betting_menu_logic, render_betting_menu, init_betting_menu
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, MAX_FPS, FLAGS, DECK_NUM, DEALED_CARD_POSSIBLE_ROTATION, DEALED_CARD_POSSIBLE_X_OFFSET_RANGE

class Game():
    def __init__(self):
        #Game inizialization
        pygame.init()
        allowed_events = [QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE, MOUSEMOTION]
        pygame.event.set_allowed(allowed_events)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS)
        self.fake_screen = self.screen.copy()
        pygame.display.set_caption("Blackjack 2")
        self.clock = pygame.time.Clock()
    
        #Game variables
        self.game_state = GameState.START_MENU
        self.player_money = 500
        self.player_health = 5
        self.dealer_health = 5
        self.player_hand = [] #Player cards
        self.thrown_cards = [] #Thrown cards
        self.dealer_cards = [] #Dealer cards
        card_objects = self.cards_objects_list("graphics/cards/normal_cards/option2")
        #card_objects = self.cards_objects_list(f"graphics/cards/normal_cards/option{random.randint(1,2)}")
        self.deck = card_objects * DECK_NUM
        self.generic_background = pygame.image.load("graphics/background.jpg").convert_alpha()

        # Start menu
        init_start_menu(self)
        #Play message
        rand_rotation_value = random.randrange(-20, 20)
        #self.start_menu_deck = pygame.image.load("graphics/cards/red_deck_right.png").convert_alpha()
        #start_menu_rect_topleft = (random.randrange(10, 100), random.randrange(10, 100)) 
        #self.start_menu_deck_rect = self.start_menu_deck.get_rect(topleft = start_menu_rect_topleft)

        #Gameplay
        self.gameplay_buttons_font = pygame.font.Font("graphics/m5x7.ttf", 68)
        self.card_width, self.card_height = self.deck[0].front_sprite.get_size() #Get the size of the card sprite
        self.cards_in_hand_y_value = SCREEN_HEIGHT - int(self.card_height * 0.6)
        init_gameplay_state(self)

        #Betting menu
        self.betting_message_font = pygame.font.Font("graphics/m5x7.ttf", 48)
        self.betting_options_font = pygame.font.Font("graphics/m5x7.ttf", 68)
        init_betting_menu(self)

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), FLAGS)
                    self.update_mouse_position(event.w, event.h)
                else:
                    temp_game_state = self.handle_gamestate_specific_events(event) 
                    self.game_state = temp_game_state if temp_game_state is not None else self.game_state

            self.update_logic()
            self.render()

            self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0, 0))
            pygame.display.flip()
            self.clock.tick(MAX_FPS)

    def handle_gamestate_specific_events(self, event):
        if self.game_state == GameState.GAMEPLAY:
            handle_gameplay_events(self, event)
        elif self.game_state == GameState.POWERUP_MENU:
            handle_powerup_menu_events(self, event)
        elif self.game_state == GameState.START_MENU:
            handle_start_menu_events(self, event)
        elif self.game_state == GameState.PAUSE_MENU:
            handle_pause_menu_events(self, event)
        elif self.game_state == GameState.BETTING_MENU:
            handle_betting_menu_events(self, event)

    def update_logic(self):
        if self.game_state == GameState.GAMEPLAY:
            update_gameplay_logic(self)
        elif self.game_state == GameState.POWERUP_MENU:
            update_powerup_menu_logic()
        elif self.game_state == GameState.START_MENU:
            update_start_menu_logic(self)
        elif self.game_state == GameState.PAUSE_MENU:
            update_pause_menu_logic()
        elif self.game_state == GameState.BETTING_MENU:
            update_betting_menu_logic()

    def render(self):
        if self.game_state == GameState.GAMEPLAY:
            render_gameplay(self)
        elif self.game_state == GameState.POWERUP_MENU:
            render_powerup_menu(self)
        elif self.game_state == GameState.START_MENU:
            render_start_menu(self)
        elif self.game_state == GameState.PAUSE_MENU:
            render_pause_menu(self)
        elif self.game_state == GameState.BETTING_MENU:
            render_betting_menu(self)

    def quit_game(self):
        pygame.quit()
        exit()

    def update_mouse_position(self, new_width, new_height):
        # Get the current mouse position
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
        # Get the current window size
        current_width, current_height = self.screen.get_size()
        # Calculate the scaling factors
        scale_x = new_width / current_width
        scale_y = new_height / current_height
        # Adjust the mouse position based on the scaling factors
        new_mouse_x = int(current_mouse_x * scale_x)
        new_mouse_y = int(current_mouse_y * scale_y)
        
        # Set the new mouse position
        pygame.mouse.set_pos((new_mouse_x, new_mouse_y))

    def cards_objects_list(self, directory):
        card_objects = []
        for filename in os.listdir(directory):
            if (filename.endswith(".png") or filename.endswith(".jpg")):
                image_path = os.path.join(directory, filename)
                loaded_image = pygame.image.load(image_path).convert_alpha()
                card_objects.append(Card(int(filename[:2]), loaded_image, True))
        return card_objects
    
    def deal_cards_to_player(self, amount):
        for _ in range(amount):
            card = random.choice(self.deck)
            card.set_owner('player')
            self.deck.remove(card)
            card.rotate(random.randrange(*DEALED_CARD_POSSIBLE_ROTATION)) #Rotate the card
            random_x_offset = random.randrange(*DEALED_CARD_POSSIBLE_X_OFFSET_RANGE)
            start_animation_x = SCREEN_WIDTH // 2 - (self.card_width // 2) + random_x_offset
            start_animation_y = -self.card_height // 2
            start_animation_rect = pygame.Rect(start_animation_x, start_animation_y, self.card_width, self.card_height)
            card.flip()  # Flip the cards on its back to hide it
            card.set_rect(start_animation_rect)
            self.thrown_cards.append(card)  # Add the card to the list of cards which are currently being animated
    
    def add_cards_to_dealer(self, amount):
        for i in range(amount):
            card = random.choice(self.deck)
            card.set_owner('dealer')
            self.deck.remove(card)
            self.thrown_cards.append(card)
            if len(self.thrown_cards) == 1: card.flip()
            if i % 2 == 0:
                start_animation_x = SCREEN_WIDTH // 2 - self.card_width - 10
            else: start_animation_x = SCREEN_WIDTH // 2 + 10
            start_animation_y = -self.card_height // 2
            start_animation_rect = pygame.Rect(start_animation_x, start_animation_y, self.card_width, self.card_height)
            card.set_rect(start_animation_rect)

    def update_player_hand_rects(self):
        num_cards = len(self.player_hand)
        total_width = num_cards * self.card_width
        start_x = (SCREEN_WIDTH - total_width) // 2

        # Update the rects of the card objects
        for i in range(num_cards):
            x = start_x + i * self.card_width + i * 5  
            rect = pygame.Rect(x, self.cards_in_hand_y_value, self.card_width, self.card_height)
            self.player_hand[i].set_rect(rect)

if __name__ == "__main__":
    game = Game()
    game.main() 