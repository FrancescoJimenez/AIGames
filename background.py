import pygame

class Background():

    def __init__(self,screen):
    
        self.screen = screen
        self.image = pygame.image.load('Sprites/Back3.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.x = 0
        self.rect.y = 0

    def blit(self):
    
            self.screen.blit(self.image, self.rect)

            