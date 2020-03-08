import pygame

class Prisoner():

    def __init__(self,settings,screen,grounds):
    
         self.screen = screen
         self.images=[]
         self.timer = 0
         self.timer2 = 0
         self.timer3 = 0
         
         self.images.append(pygame.image.load('Sprites/running/Run1.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run2.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run3.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run4.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run5.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run6.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run7.png').convert_alpha())
         self.images.append(pygame.image.load('Sprites/running/Run8.png').convert_alpha())
         
         self.image_jump = []
         self.image_jump.append(pygame.image.load('Sprites/running/Jump1.png').convert_alpha())
         self.image_jump.append(pygame.image.load('Sprites/running/Jump3.png').convert_alpha())
         self.image_jump.append(pygame.image.load('Sprites/running/Jump4.png').convert_alpha())
         
         self.image_jump2 = []
         self.image_jump2.append(pygame.image.load('Sprites/running/Jump12.png').convert_alpha())
         self.image_jump2.append(pygame.image.load('Sprites/running/Jump22.png').convert_alpha())
         self.image_jump2.append(pygame.image.load('Sprites/running/Jump32.png').convert_alpha())
         
         self.image_death = pygame.image.load('Sprites/running/Death.png').convert_alpha()
         
         
         self.image_jump_descent = pygame.image.load('Sprites/running/Jump2.png').convert_alpha()

         self.index = 0
         self.index_jump = 0
         self.index_jump2 = 0
         self.image = self.images[self.index] 
         self.up_flag = True
         self.down_flag = False
         self.animation_flag = False
         
         self.mask = pygame.mask.from_surface(self.image)

         self.rect = self.image.get_rect()
         self.screen_rect = screen.get_rect()
         self.settings = settings
         
         for ground in grounds.copy():
             self.rect.bottom = ground.rect.top
             self.jump_speed = settings.jump_add_constant
         self.rect.x = self.settings.prisoner_position
         
         self.y = float(self.rect.y)
         
    def update(self,settings,grounds):
    
        if settings.jump_flag:
        
            if settings.jump_type:
                self.y -= settings.jump_sprint
            else:
                self.y -= settings.jump_sprint2
            if self.rect.bottom < settings.jump_limit:
                settings.jump_flag = False
                settings.jump_descent = True
            self.rect.y = self.y
            
        
        elif settings.jump_descent:
        
            self.jump_speed -= settings.jump_decrease_constant
            self.y -= self.jump_speed
            
            if self.jump_speed > 0 and settings.decrease_ground:
            
                settings.ground_speed -= settings.decrease
                settings.decrease_ground = False
     
            for ground in grounds.copy():
                    if self.rect.bottom > ground.rect.top:
                        settings.jump_flag = False
                        settings.jump_descent = False
                        self.animation_flag = False
                        settings.jump_type = True
                        self.jump_speed = settings.jump_add_constant
                        self.rect.bottom = ground.rect.top
                    else:
                        self.rect.y = self.y
                        
        self.rect.x = settings.prisoner_position 
                    
    def blitme(self,settings,grounds):
    
        if not settings.game_active and not settings.jump_descent and not settings.jump_flag:
        
            self.image = self.image_death
            self.screen.blit(self.image,self.rect)
            for ground in grounds.copy():
                self.rect.bottom = ground.rect.top + 35
        
        else: 
        
            if not self.animation_flag:
                self.timer += 1
                if self.timer > settings.prisoner_animation_speed:
                    self.index += 1
                    self.timer = 0
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
                self.mask = pygame.mask.from_surface(self.image)
                self.screen.blit(self.image, self.rect)
                
            elif not settings.jump_descent or self.jump_speed > 0:
            
                if settings.jump_type:
                    self.timer2 += 1
                    if self.timer2 > 8:
                        self.index_jump += 1
                        self.timer2 = 0
                    if self.index_jump >= len(self.image_jump):
                        self.index_jump = 0
                    self.image = self.image_jump[self.index_jump]
                    self.mask = pygame.mask.from_surface(self.image)
                    self.screen.blit(self.image,self.rect)
                    
                else:
                    self.timer3 += 1
                    if self.timer3 > 8:
                        self.index_jump2 += 1
                        self.timer2 = 0
                    if self.index_jump2 >= len(self.image_jump2):
                        self.index_jump2 = 0
                    self.image = self.image_jump2[self.index_jump2]
                    self.mask = pygame.mask.from_surface(self.image)
                    self.screen.blit(self.image,self.rect)
                
            else:
                self.image = self.image_jump_descent
                self.mask = pygame.mask.from_surface(self.image)
                self.screen.blit(self.image,self.rect)
