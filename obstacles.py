import pygame

from random import randint
from pygame.sprite import Sprite

class Obstacles(Sprite):

        def __init__(self,settings,screen,grounds):
            
            self.screen = screen
            
            self.images = []
            self.images.append(pygame.image.load('Sprites/Rocks.bmp'))
            self.images.append(pygame.image.load('Sprites/Rock2.bmp'))
            self.images.append(pygame.image.load('Sprites/Rock3.bmp'))
            self.images.append(pygame.image.load('Sprites/Rock4.bmp'))
            self.images.append(pygame.image.load('Sprites/Tree1.bmp'))
            self.images.append(pygame.image.load('Sprites/Log1.bmp'))
            self.images.append(pygame.image.load('Sprites/Log2.bmp'))
            self.images.append(pygame.image.load('Sprites/Log3.bmp'))
            self.images.append(pygame.image.load('Sprites/Bush.bmp'))

            self.index = 0
            
            self.image = self.images[self.index]
            
            self.rect = self.image.get_rect()
            self.screen_rect = screen.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            
            self.flag = False
            
            self.rect.bottom = self.screen_rect.bottom
            self.rect.left = self.screen_rect.right
            self.x = float(self.rect.x)
            
        def update(self,settings,ob,obs):
        
            if settings.game_active:
                self.x -= settings.ground_speed
               
                if ob.rect.right < 0:
                    obs.remove(ob)
                self.rect.x = self.x
            
            elif not settings.game_active and (settings.jump_flag or settings.jump_descent):
                self.x  -= settings.ground_speed
                self.rect.x = self.x
            
        
        def pick_obstacle(self,grounds):
            
            self.image = self.images[self.index]
            self.image.set_colorkey(0,0)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            
            for ground in grounds.copy():
                self.rect.bottom = ground.rect.top
                
                
        def blitme(self):
            
            self.screen.blit(self.image, self.rect)
                