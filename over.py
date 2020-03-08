import pygame
from button import Button

class Over():

    def __init__(self,screen):
    
        self.screen = screen
        self.images = []
        self.images.append(pygame.image.load('Sprites/GameOver/Over1.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/GameOver/Over2.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/GameOver/Over3.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/GameOver/Over4.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/GameOver/Over5.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/GameOver/Over6.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/GameOver/Over7.png').convert_alpha())
        
        self.index = 0
        self.timer = 0
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx 
        self.rect.centery = self.screen_rect.centery - 100

    def blit(self,settings):
    
        if not settings.game_active and not settings.jump_descent and not settings.jump_flag:
            if self.index != len(self.images)-1:
                self.timer += 1
                if self.timer > 10:
                    self.index += 1
                    self.timer = 0
            self.image = self.images[self.index]

            self.screen.blit(self.image, self.rect)