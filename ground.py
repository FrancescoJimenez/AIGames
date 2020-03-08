
import pygame
from pygame.sprite import Sprite
from random import randint

class Ground(Sprite):

    def __init__(self,settings,screen):
        
        super().__init__()
        self.screen = screen
        
        self.images = []
        self.images.append(pygame.image.load('Sprites/ground/Ground.bmp').convert_alpha())
        self.images.append(pygame.image.load('Sprites/ground/Ground2.bmp').convert_alpha())
        self.images.append(pygame.image.load('Sprites/ground/Ground3.bmp').convert_alpha())
        self.images.append(pygame.image.load('Sprites/ground/Ground4.bmp').convert_alpha())
        self.index = 0
        
        self.image = self.images[self.index]
        
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.bottom = self.screen_rect.bottom
        self.rect.centerx = self.screen_rect.centerx
        self.flag = False
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self,settings):
        
        if settings.game_active:
            self.x -= settings.ground_speed
            self.rect.x = self.x
        elif not settings.game_active and (settings.jump_flag or settings.jump_descent):
            self.x  -= settings.ground_speed
            self.rect.x = self.x
            
    def blitme(self):

        self.screen.blit(self.images[self.index], self.rect)
