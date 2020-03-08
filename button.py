import pygame


class Button():

    def __init__(self,screen,settings):
        
        self.screen = screen
        
        self.images = []
        self.images.append(pygame.image.load('Sprites/1.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/2.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/3.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/4.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/5.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/6.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/7.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/8.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/9.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/10.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/9.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/8.png').convert_alpha())
        self.images.append(pygame.image.load('Sprites/7.png').convert_alpha())
        
        self.timer = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.center = self.screen_rect.center
        self.rect.centery = self.screen_rect.centery + 20
        
    def blitme(self,settings):
    
        if not settings.game_active and not settings.jump_descent and not settings.jump_flag:
        
            self.timer += 1
            if self.timer > 10:
                self.index += 1
                self.timer = 0
            if self.index == len(self.images):
                self.index = 9
            self.image = self.images[self.index]
            self.screen.blit(self.image, self.rect)