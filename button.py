import pygame
from colores import *


class Widget:
    def __init__(self):
        pass

    def render(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class Button(Widget):
    def __init__(self, surface, image_path, x, y,width,height):
        super().__init__()
        self.master_surface = surface
        self.slave_surface = pygame.image.load(image_path).convert_alpha()
        self.slave_surface = pygame.transform.scale(self.slave_surface, (width, height))
        self.slave_rect = self.slave_surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y

    def render(self):
        pass

    def update(self):
        self.render()


    def draw(self):
        self.master_surface.blit(self.slave_surface, self.slave_rect)

    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.slave_rect.collidepoint(mouse_pos)



class TextBox(Widget):
    def __init__(self, surface, x, y, width, height, font_size):
        super().__init__()
        self.master_surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.text = ""

    def render(self):
        pygame.draw.rect(self.master_surface,blanco, self.rect, 2)

    def update(self):
        self.render()

    def draw(self):
            text_surface = self.font.render(self.text, True,negro)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.master_surface.blit(text_surface, text_rect)
