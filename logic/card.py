import pygame

class Card:
    def __init__(self, name, sprite, visible):
        self.name = name
        self.sprite = sprite
        self.visible = visible
        self.rect = None
        self.hidden_sprite = pygame.image.load("graphics/cards/normal_cards/back.png").convert_alpha()

    def set_rect(self, rect):
        self.rect = rect

    def draw(self, screen):
        if self.visible: screen.blit(self.sprite, self.rect)
        else: screen.blit(self.hidden_sprite, self.rect)