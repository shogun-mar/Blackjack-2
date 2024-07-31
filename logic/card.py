import pygame

class Card:
    def __init__(self, name, sprite, visible):
        self.name = name
        self.rect = None
        self.visible = visible
        self.rotation_value = None
        self.front_sprite = sprite
        self.back_sprite = pygame.image.load("graphics/cards/normal_cards/back.png").convert_alpha()
        self.sprite_width, self.sprite_height = self.front_sprite.get_size()

    def set_rect(self, rect):
        self.rect = rect

    def flip(self):
        self.visible = not self.visible

    def rotate(self):
        self.front_sprite = pygame.transform.rotate(self.front_sprite, self.rotation_value)
        self.back_sprite = pygame.transform.rotate(self.back_sprite, self.rotation_value)

    def reset_rotation(self):
        self.front_sprite = pygame.transform.rotate(self.front_sprite, 360 - self.rotation_value)
        self.back_sprite = pygame.transform.rotate(self.back_sprite, 360 - self.rotation_value)

    def reset_surf_size(self):
        self.front_sprite = pygame.transform.smoothscale(self.front_sprite, (self.sprite_width, self.sprite_height))
        self.back_sprite = pygame.transform.smoothscale(self.back_sprite, (self.sprite_width, self.sprite_height))

    def draw(self, screen):
        if self.visible:
            screen.blit(self.front_sprite, self.rect)
        else:
            screen.blit(self.back_sprite, self.rect)