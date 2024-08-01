from enum import Enum

class GameState(Enum):
    GAMEPLAY = 0
    POWERUP_MENU = 1
    START_MENU = 2
    PAUSE_MENU = 3
    BETTING_MENU = 4