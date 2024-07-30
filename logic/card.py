import pygame

class Card:
    def __init__(self, name, sprite, visible):
        self.name = name
        self.rect = None
        self.visible = visible
        self.front_sprite = sprite
        self.back_sprite = pygame.image.load("graphics/cards/normal_cards/back.png").convert_alpha()

    def set_rect(self, rect):
        self.rect = rect

    def flip(self):
        self.visible = not self.visible

    def rotate(self, value):
        self.front_sprite = pygame.transform.rotate(self.front_sprite, value)
        self.back_sprite = pygame.transform.rotate(self.back_sprite, value)

    def draw(self, screen):
        if self.visible:
            screen.blit(self.front_sprite, self.rect)
        else:
            screen.blit(self.back_sprite, self.rect)