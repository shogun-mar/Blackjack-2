import pygame, os
from states.gameState import GameState
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE
from states.gameplay import handle_gameplay_events, update_gameplay_logic, render_gameplay
from states.powerupMenu import handle_powerup_menu_events, update_powerup_menu_logic, render_powerup_menu
from states.startMenu import handle_start_menu_events, update_start_menu_logic, render_start_menu
from states.pauseMenu import handle_pause_menu_events, update_pause_menu_logic, render_pause_menu
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, MAX_FPS, FLAGS

class Game():
    def __init__(self):
        #Game inizialization
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS)
        self.fake_screen = self.screen.copy()
        pygame.display.set_caption("Blackjack 2")
        # Define allowed events
        allowed_events = [QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE]
        pygame.event.set_allowed(allowed_events)
        self.clock = pygame.time.Clock()
    
        #Game variables
        self.game_state = GameState.START_MENU
        self.player_hand = {}
        self.cards_dict = self.load_images_to_dictionary("graphics/cards/normal_cards")

        #Start menu
        self.background = pygame.image.load("graphics/background.jpg").convert_alpha()

        font = pygame.font.Font("graphics/m5x7.ttf", 36)
        self.play_message = font.render("Press SPACE to play!", True, (255, 255, 255))
        self.play_message_original = self.play_message.copy()
        self.play_message_original_size = self.play_message.get_size()
        self.play_message_rect = self.play_message.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), FLAGS)
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
            update_gameplay_logic()
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

    def load_images_to_dictionary(self, directory):
        images = {}
        for filename in os.listdir(directory):
            if filename.endswith(".png") or filename.endswith(".jpg"):  # Add other extensions if needed
                image_path = os.path.join(directory, filename)
                images[filename] = pygame.image.load(image_path).convert_alpha()
        return images

    def quit_game(self):
        pygame.quit()
        exit()

if __name__ == "__main__":
    game = Game()
    game.main() 