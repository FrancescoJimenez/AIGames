import pygame
import json

class Text():

    def __init__(self,settings,screen):
        
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        Size = 40
        text_default = "Score: 0"
        self.f = pygame.font.Font("Sprites/New.ttf",Size)
        self.colour = (255,255,255)
        self.textSurface = self.f.render(text_default, True, self.colour)
        self.TextRect = self.textSurface.get_rect()
        self.width = self.TextRect.width
        self.height = self.TextRect.height
        self.TextRect.x = 20
        self.TextRect.y = 20
        self.blitme()
        
        
    def text_object(self,text,f):
    
        self.textSurface = f.render(text, True, (255,255,255))
        return self.textSurface, self.textSurface.get_rect()
        
    def score_display(self,text,settings,screen):
    
        Size = 40
        self.f = pygame.font.Font("Sprites/New.ttf",Size)
        self.textSurface, self.TextRect = self.text_object(text, self.f)
        self.TextRect.x = 20
        self.TextRect.y = 20
        self.blitme()
        
    def update_score(self,settings,screen):
    
        Score_text = "Score:" + str(settings.score)
        self.score_display(Score_text,settings,screen)
        
    def blitme(self):
        
        self.screen.blit(self.textSurface, self.TextRect)
    
class Top():

    def __init__(self,settings,screen):
        
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        Size = 20
        try: 
            filename = "score.json"
            with open(filename) as f_obj:
                self.Top_S = json.load(f_obj)
                text_default = "Top Score: " + str(self.Top_S)
        except FileNotFoundError:
            text_default = "Top Score: 0"
            self.Top_S = 0
        self.f = pygame.font.Font("Sprites/New.ttf",Size)
        self.colour = (0,255,0)
        self.textSurface = self.f.render(text_default, True, self.colour)
        self.TextRect = self.textSurface.get_rect()
        self.TextRect.x = 20
        self.TextRect.y = 70
        self.blitme()
        
        
    def text_object(self,text,f):
        
        self.textSurface = f.render(text, True, (255,255,0))
        return self.textSurface, self.textSurface.get_rect()
        
    def top_display(self,text,settings,screen):
    
        Size = 20
        self.f = pygame.font.Font("Sprites/New.ttf",Size)
        self.textSurface, self.TextRect = self.text_object(text, self.f)
        self.TextRect.x = 20
        self.TextRect.y = 70
        self.blitme()
        
    def update_top(self,settings,screen):
    
        Top_text = "Top Score:" + str(self.Top_S)
        self.top_display(Top_text,settings,screen)
        
    def blitme(self):
        
        self.screen.blit(self.textSurface, self.TextRect)