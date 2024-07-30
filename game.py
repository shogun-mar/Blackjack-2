import pygame, os, random
from logic.states.gameState import GameState
from logic.card import Card
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE, MOUSEMOTION
from logic.states.gameplay import handle_gameplay_events, update_gameplay_logic, render_gameplay
from logic.states.powerupMenu import handle_powerup_menu_events, update_powerup_menu_logic, render_powerup_menu
from logic.states.startMenu import handle_start_menu_events, update_start_menu_logic, render_start_menu
from logic.states.pauseMenu import handle_pause_menu_events, update_pause_menu_logic, render_pause_menu
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, MAX_FPS, FLAGS, DECK_NUM, DEALED_CARD_POSSIBLE_ROTATION

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
        self.player_hand = []
        self.player_hand_rects = []
        self.cards_on_table = []
        self.card_objects = self.cards_objects_list("graphics/cards/normal_cards")
        self.deck = self.card_objects * DECK_NUM

        #Start menu
        self.background = pygame.image.load("graphics/background.jpg").convert_alpha()

        font = pygame.font.Font("graphics/m5x7.ttf", 36)
        self.play_message = font.render("Press SPACE to play!", True, (255, 255, 255))
        self.play_message_original = self.play_message.copy()
        self.play_message_original_size = self.play_message.get_size()
        self.play_message_rect = self.play_message.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

        #Gameplay
        self.card_width, self.card_height = self.card_objects[0].sprite.get_size() #Get the size of the card sprite
        self.cards_in_hand_y_value = SCREEN_HEIGHT // 2 - self.card_height // 2 + 375

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

    def update_logic(self):
        if self.game_state == GameState.GAMEPLAY:
            update_gameplay_logic(self)
        elif self.game_state == GameState.POWERUP_MENU:
            update_powerup_menu_logic()
        elif self.game_state == GameState.START_MENU:
            update_start_menu_logic(self)
        elif self.game_state == GameState.PAUSE_MENU:
            update_pause_menu_logic()

    def render(self):
        if self.game_state == GameState.GAMEPLAY:
            render_gameplay(self)
        elif self.game_state == GameState.POWERUP_MENU:
            render_powerup_menu(self)
        elif self.game_state == GameState.START_MENU:
            render_start_menu(self)
        elif self.game_state == GameState.PAUSE_MENU:
            render_pause_menu(self)

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
            if (filename.endswith(".png") or filename.endswith(".jpg")) and filename != "back.png":  # Add other extensions if needed
                image_path = os.path.join(directory, filename)
                card_objects.append(Card(filename, pygame.image.load(image_path).convert_alpha(), True))
        return card_objects
    
    def deal_card_to_player(self):
        card = random.choice(self.deck)
        card.sprite = pygame.transform.rotate(DEALED_CARD_POSSIBLE_ROTATION)
        start_animation_rect = pygame.Rect(SCREEN_WIDTH // 2, -game.card_height // 2, self.card_width, self.card_height)
        card.set_rect(start_animation_rect)
        self.deck.remove(card)
        self.cards_on_table.append(card)

    def bind_player_hand_rects(self):
        self.player_hand_rects = self.create_player_hand_rects() #Create rects for each card in player_hand with the position based on the number of cards
        for i in range(len(self.player_hand)):
            self.player_hand[i].set_rect(self.player_hand_rects[i])

    def update_player_hand_rects(self):
        rects = []
        num_cards = len(self.player_hand)
        
        if num_cards == 0: raise ValueError("No cards to create rects for") # No cards to create rects for

        total_width = num_cards * self.card_width
        start_x = (SCREEN_WIDTH - total_width) // 2

        self.player_hand_rects.clear()  # Clear any existing rects

        for i in range(num_cards):
            x = start_x + i * self.card_width
            rect = pygame.Rect(x, self.cards_in_hand_y_value, self.card_width, self.card_height)
            rects.append(rect)

        return rects

if __name__ == "__main__":
    game = Game()
    game.main() 