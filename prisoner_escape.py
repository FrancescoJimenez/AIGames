import pygame
import neat
import os

from random import randint
from settings import Settings1
from ground import Ground
from prisoner import Prisoner
from obstacles import Obstacles
from score_text import Text,Top
import game_functions as gf
from pygame.sprite import Group
from second_level import Obstacles2
from background import Background as bg
from button import Button
from over import Over
from settings2 import Settings2

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30,50)
STAT_FONT = pygame.font.Font(r"C:\Users\gover\Desktop\Prisoner_escape\Sprites\New.ttf",30)
STAT_FONT2 = pygame.font.Font(r"C:\Users\gover\Desktop\Prisoner_escape\Sprites\New.ttf",20)
GEN = 0

def run_game(genomes,config):

    global GEN
    GEN += 1
    nets = []
    ge = []   
    obs = []
    prisoners = [] 
    settingsP = []
    settings = Settings1()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height)) 
    pygame.display.set_caption("Prison Escape AI")
    grounds = Group()
    ground = Ground(settings,screen)
    grounds.add(ground)
    color_blink = False
    counter = 0
    
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        settingsP.append(Settings2())
        prisoners.append(Prisoner(settingsP[0],screen,grounds))
        g.fitness = 0
        ge.append(g)
    
    pygame.mixer.music.load("Sounds/Gaur.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    obs2 = Group()
    
    background = bg(screen)
    over = Over(screen)
    top = Top(settings,screen)
    over_b = Button(screen,settings)
    text = Text(settings,screen)

    
    s = pygame.Surface((settings.screen_width,settings.screen_height))  
    s.set_alpha(settings.alpha_value)
    s.fill((0,0,0))
    
    
    while True:
    
        gf.check_events(prisoners,grounds,settings,obs,obs2,over_b,screen,top)
        if not len(prisoners) > 0:
            break
        screen.fill(settings.bg_colour)
        if settings.game_active:
        
            screen.fill(settings.bg_colour)
            gf.increase_diff(settings,grounds,settingsP)
            gf.generate_obstacle(settings,obs,grounds,screen)
            gf.generate_obstacle2(settings,obs2,grounds,screen)
            
            for x, prisoner in enumerate(prisoners):
                if gf.player_object_collisions(prisoner,obs,settings):
            
                    if len(obs) > 0:
                        if prisoner.rect.bottom > obs[0].rect.bottom :
                            ge[x].fitness += 1
                        if prisoner.rect.left > obs[-1].rect.right:             
                            ge[x].fitness += 1
                    ge[x].fitness -= 5        
                    prisoners.pop(x)
                    settingsP.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    color_blink = True
                    counter = 0

        for x,prisoner in enumerate(prisoners):
            prisoner.update(settingsP[x],grounds)
            ge[x].fitness += 0.1   
            if len(obs) > 0:
                output = nets[x].activate((prisoner.rect.bottom,abs(prisoner.rect.right - obs[0].x),abs(prisoner.rect.right - obs[-1].x),abs(prisoner.rect.bottom - obs[0].rect.top),abs(prisoner.rect.bottom - obs[-1].rect.top)))
            
                if output[0] > 0.6 and not settingsP[x].jump_descent and not settingsP[x].jump_flag: 
                    settingsP[x].jump_flag = True
                    prisoner.animation_flag = True
                    settingsP[x].jump_type = True 
                    settingsP[x].jump_sound.set_volume(0.1)
                    settingsP[x].jump_sound.play()
                    
                if output[1] > 0.5 and settingsP[x].jump_flag:
                    settingsP[x].jump_flag = False
                    settingsP[x].jump_descent = True
                    settingsP[x].jump_type = True                   
     
        for ob in obs:
            ob.update(settings,ob,obs)
        obs2.update(settings,obs2)
        gf.update_ground(settings,screen,grounds)
        gf.update_screen(settingsP,grounds,prisoners,obs,text,screen,background,obs2,top,settings)
        
        text2 = STAT_FONT.render("Gen:" + str(GEN), 1,(255,255,255))
        screen.blit(text2,(17,110)) 
    
        if color_blink:
            text3 = STAT_FONT2.render("Players: " + str(len(prisoners)), 1,(0,255,255))
            screen.blit(text3,(17,120 + text2.get_height())) 
            counter += 1
            if counter > 30:
                color_blink = False
                counter = 0 
        else:
            text3 = STAT_FONT2.render("Players: " + str(len(prisoners)), 1,(0,225,255))
            screen.blit(text3,(17,120 + text2.get_height())) 
               
        pygame.display.flip()
       

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(run_game,50)
    
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"Config.txt")
    run(config_path)
