import pygame
from constantes import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,direccion,img):
        super().__init__()
        self.image = img
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = direccion

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
