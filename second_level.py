import pygame

from random import randint
from pygame.sprite import Sprite

class Obstacles2(Sprite):

        def __init__(self,settings,screen,grounds):
            
            super().__init__()
            self.screen = screen
            
            self.images = []
            self.images.append(pygame.image.load('Sprites/Big_Tree2.png').convert_alpha())
            self.images.append(pygame.image.load('Sprites/Big_Tree3.png').convert_alpha())
            self.images.append(pygame.image.load('Sprites/Monster.png').convert_alpha())
            self.images.append(pygame.image.load('Sprites/Troll.png').convert_alpha())
            self.images.append(pygame.image.load('Sprites/Big_Tree4.png').convert_alpha())

            self.images_troll = []
            self.images_troll.append(pygame.image.load('Sprites/Troll.png').convert_alpha())
            self.images_troll.append(pygame.image.load('Sprites/Troll2.png').convert_alpha())
            self.images_troll.append(pygame.image.load('Sprites/Troll3.png').convert_alpha())
            self.images_troll.append(pygame.image.load('Sprites/Troll2.png').convert_alpha())
            self.images_troll.append(pygame.image.load('Sprites/Troll.png').convert_alpha())
            
            self.images_monster = []
            self.images_monster.append(pygame.image.load('Sprites/Monster.png').convert_alpha())
            self.images_monster.append(pygame.image.load('Sprites/Monster2.png').convert_alpha())
            self.images_monster.append(pygame.image.load('Sprites/Monster3.png').convert_alpha())
            self.images_monster.append(pygame.image.load('Sprites/Monster2.png').convert_alpha())
            self.images_monster.append(pygame.image.load('Sprites/Monster.png').convert_alpha())
            
            self.index = 0
            self.index_troll = 0
            self.index_monster = 0
            self.timer = 0
            self.timer2 = 0
            
            self.image = self.images[self.index]
            self.image_troll = self.images_troll[self.index_troll]
            self.image_monster = self.images_monster[self.index_monster]
            
            self.rect = self.image.get_rect()
            self.screen_rect = screen.get_rect()
            
            self.flag = False
            
            self.rect.bottom = self.screen_rect.bottom
            self.rect.left = self.screen_rect.right
            self.x = float(self.rect.x)
            
        def update(self,settings,obs2):
        
            if settings.game_active:
            
                self.x -= settings.ground_speed/2
                if self.index == 2 or self.index == 3:
                    self.x -= 1
                for ob2 in obs2.copy():
                    if ob2.rect.right < 0:
                        obs2.remove(ob2)
                self.rect.x = self.x
                
            elif (not settings.game_active and (settings.jump_flag or settings.jump_descent)) or self.index == 2 or self.index == 3:
            
                for ob2 in obs2.copy():
                    if ob2.rect.right < 0:
                        obs2.remove(ob2)
                self.x  -= settings.ground_speed/2
                
                self.rect.x = self.x
        
        def pick_obstacle(self,grounds):
            
            if self.index == 3:
                self.image = self.images_troll[self.index_troll]
            elif self.index == 2:
                self.image = self.images_monster[self.index_monster]
                
            else:
                self.image = self.images[self.index]
            self.image.set_colorkey(0,0)
            self.rect = self.image.get_rect()
            
            for ground in grounds.copy():
                self.rect.bottom = ground.rect.top + 50
                
                
        def blitme(self):
            
            if self.index == 3:
                self.timer += 1
                if self.timer > 20:
                    self.index_troll += 1
                    self.timer = 0
                if self.index_troll >= len(self.images_troll):
                    self.index_troll = 0
                self.image = self.images_troll[self.index_troll]
                
            elif self.index == 2:
                self.timer2 += 1
                if self.timer2 > 20:
                    self.index_monster += 1
                    self.timer2 = 0
                if self.index_monster >= len(self.images_monster):
                    self.index_monster = 0
                self.image = self.images_monster[self.index_monster]
                
            self.screen.blit(self.image, self.rect)