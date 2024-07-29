import pygame
from states.gameState import GameState
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, MAX_FPS, FLAGS

class Game():
    def __init__(self):
        #Game inizialization
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS)
        self.fake_screen = self.screen.copy()
        pygame.display.set_caption("Blackjack 2")
        self.clock = pygame.time.Clock()
    
        #Game variables
        self.game_state = GameState.START_MENU

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), FLAGS)
                self.game_state = self.handle_gamestate_specific_events(event)

            self.update_logic()
            self.render()

            self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0, 0))
            pygame.display.flip()
            self.clock.tick(MAX_FPS)

    def handle_gamestate_specific_events(self, event):
        if self.game_state == GameState.GAMEPLAY:
            handle_gameplay_events(event)
        elif self.game_state == GameState.POWERUP_MENU:
            handle_powerup_menu_events(event)
        elif self.game_state == GameState.START_MENU:
            handle_start_menu_events(event)
        elif self.game_state == GameState.PAUSE_MENU:
            handle_pause_menu_events(event)

    def update_logic(self):
        if self.game_state == GameState.GAMEPLAY:
            update_gameplay_logic()
        elif self.game_state == GameState.POWERUP_MENU:
            update_powerup_menu_logic()
        elif self.game_state == GameState.START_MENU:
            update_start_menu_logic()
        elif self.game_state == GameState.PAUSE_MENU:
            update_pause_menu_logic()

    def render(self):
        if self.game_state == GameState.GAMEPLAY:
            render_gameplay(self.fake_screen)
        elif self.game_state == GameState.POWERUP_MENU:
            update_powerup_menu(self.fake_screen)
        elif self.game_state == GameState.START_MENU:
            render_start_menu(self.fake_screen)
        elif self.game_state == GameState.PAUSE_MENU:
            render_pause_menu(self.fake_screen)

    def quit_game(self):
        pygame.quit()
        exit()