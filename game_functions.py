import pygame
import sys
import json

from ground import Ground
from obstacles import Obstacles
from second_level import Obstacles2
from score_text import Top
from random import randint

def check_events(prisoner,grounds,settings,obs,obs2,over_b,screen,top):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
    
        elif event.type == pygame.KEYDOWN:
            check_keydown(event,prisoner,grounds,settings,obs,obs2,over_b,screen)
            
        elif event.type == pygame.KEYUP:
            check_keyup(event,prisoner,grounds,settings)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_over_button(mouse_x,mouse_y,screen,settings,obs,obs2,prisoner,grounds,over_b,top)
            
def check_keydown(event,prisoner,grounds,settings,obs,obs2,over_b,screen):

        if event.key == pygame.K_SPACE and not settings.jump_descent:
            
            settings.jump_flag = True
            prisoner.animation_flag = True
            settings.jump_type = True
            settings.jump_sound.set_volume(0.6)
            #settings.jump_sound.play()
            
        if event.key == pygame.K_LSHIFT and not settings.jump_descent:
            
            settings.jump_flag = True
            prisoner.animation_flag = True
            settings.jump_type = False
            settings.decrease_ground = True
            settings.ground_speed *= 1.50
            settings.jump_sound.set_volume(0.6)
            #settings.jump_sound.play()
            settings.decrease = settings.ground_speed - settings.ground_speed/1.50
            
            
def check_over_button(mouse_x,mouse_y,screen,settings,obs,obs2,prisoner,grounds,over_b,top):
    
        if over_b.rect.collidepoint(mouse_x, mouse_y) and not settings.game_active:
            grounds.empty()
            obs.empty()
            obs2.empty()
            settings.__init__()
            ground = Ground(settings,screen)
            grounds.add(ground)
            for ground in grounds.copy():
                prisoner.rect.bottom = ground.rect.top
            top.__init__(settings,screen)
            pygame.mixer.music.load("Sounds/Gaur.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            
                
def check_keyup(event,prisoner,grounds,settings):

        if event.key == pygame.K_SPACE:
        
            if prisoner.jump_speed > 0:
                settings.jump_sound.fadeout(2000)
            settings.jump_flag = False
            settings.jump_descent = True
            settings.jump_type = True
            
        if event.key == pygame.K_LSHIFT:
            
            if prisoner.jump_speed > 0:
                settings.jump_sound.fadeout(2000)
            settings.jump_flag = False
            settings.jump_descent = True
            settings.jump_type = True
        
            if settings.decrease_ground:
                
                settings.ground_speed -= settings.decrease
                settings.decrease_ground = False
            
                
def update_ground(settings,screen,grounds):

    screen_rect = screen.get_rect()
    grounds.update(settings)
    
    for ground in grounds.copy():
    
        if ground.rect.right < 0:
            grounds.remove(ground)
        
        if ground.rect.right < screen_rect.right:
        
            if len(grounds) == 1:
            
                random_number = randint(0,3)
                if random_number == settings.store_n:
                       random_number = randint(0,3)
                new_ground = Ground(settings,screen)
                new_ground.index = random_number
                settings.store_n = random_number
                    
                new_ground.x = screen_rect.right-30
                grounds.add(new_ground)
                
def increase_diff(settings,grounds,settingsP):
    
    settings.diff_score += 1
    if settings.diff_score > 3000:
   
        settings.ground_speed += 2
        for setting in settingsP:
            setting.prisoner_animation_speed *= 0.70
        settings.diff_score = 0
        settings.ob_number += 1

        
def player_object_collisions(prisoner,obs,settings):
            
    if pygame.sprite.spritecollideany(prisoner, obs, pygame.sprite.collide_mask):
               
        settings.death_sound.set_volume(0.1)
        settings.death_sound.play()
        
        filename = "score.json"
        total_score = settings.score
        try:
            with open(filename) as f_obj:
                Top_score = json.load(f_obj)
                if total_score > Top_score:
                    with open(filename,"w") as f_obj:
                        json.dump(total_score,f_obj)
                    Top_score = total_score
                    
                
        except FileNotFoundError:
            with open(filename,"w") as f_obj:
                json.dump(total_score,f_obj)
                Top_score = total_score
        
        return True
                
            
                
def generate_obstacle(settings,obs,grounds,screen):

    random_number = randint(1,settings.spawn_chance)
    
    if not settings.ob_flag:
        
        settings.ob_timer += 1
            
        if settings.ob_timer > settings.ob_limit:
                
            settings.ob_flag = True
            settings.ob_timer = 0
    
    
    if settings.ob_flag:
    
        settings.ob_timer_spawn += 1
        
        if settings.ob_timer_spawn > settings.ob_limit_spawn:
            
            settings.ob_timer_spawn = 0
            random_number = 1
                
    if random_number == 1 and settings.ob_flag:
        
        settings.ob_flag = False
        create_obstacle(settings,obs,grounds,screen)
                
def create_obstacle(settings,obs,grounds,screen):
    
    random_number2 = randint(settings.ob_number-2,settings.ob_number)
    for x in range(1,random_number2):
    
        ob = Obstacles(settings,screen,grounds)
        random_number = randint(0,len(ob.images)-1)
        ob.index = random_number
        
        ob.pick_obstacle(grounds)
        
        if x != 1:
            if x != random_number2:
                random_offset = randint(-20,20)
            ob.x += settings.previous_position + random_offset
        settings.previous_position += ob.rect.width
        obs.append(ob)
    settings.previous_position = 0
    
def generate_obstacle2(settings,obs2,grounds,screen):

    random_number2 = randint(1,settings.spawn_chance)
    
    if not settings.ob_flag2:
        
        settings.ob_timer2 += 1
            
        if settings.ob_timer2 > settings.ob_limit2:
                
            settings.ob_flag2 = True
            settings.ob_timer2 = 0
                
    if random_number2 == 1 and settings.ob_flag2:
        
        settings.ob_flag2 = False
        create_obstacle2(settings,obs2,grounds,screen)
        
def create_obstacle2(settings,obs2,grounds,screen):
    
    random_number3 = randint(settings.ob_number2-2,settings.ob_number2)
    for x in range(1,random_number3):
    
        ob2 = Obstacles2(settings,screen,grounds)
        random_number4 = randint(0,len(ob2.images)-1)
        ob2.index = random_number4
        
        ob2.pick_obstacle(grounds)
        
        if x != 1:
            if x != random_number3:
                random_offset2 = randint(-40,40)
            ob2.x += settings.previous_position2 + random_offset2
        settings.previous_position2 += ob2.rect.width
        obs2.add(ob2)
    settings.previous_position2 = 0

def update_screen(settingsP,grounds,prisoners,obs,text,screen,background,obs2,top,settings):

    background.blit()
    
    for ob2 in obs2.sprites():
        ob2.blitme()
    
    if len(prisoners) > 0:
        for prisoner in prisoners:
            if len(obs) > 0:
                pygame.draw.line(screen, (255,0,0), (prisoner.rect.centerx,prisoner.rect.centery), (obs[0].x,obs[0].rect.bottom),2)
                pygame.draw.line(screen, (255,0,0), (prisoner.rect.centerx,prisoner.rect.centery), (obs[0].rect.centerx,obs[0].rect.top),2)
                pygame.draw.line(screen, (255,0,0), (prisoner.rect.centerx,prisoner.rect.centery), (obs[-1].x,obs[-1].rect.bottom),2)
                pygame.draw.line(screen, (255,0,0), (prisoner.rect.centerx,prisoner.rect.centery), (obs[-1].rect.centerx,obs[-1].rect.top),2)
                
    for ground in grounds.sprites():
        ground.blitme()
    
    for ob in obs:
        ob.blitme()
    
    for x,prisoner in enumerate(prisoners):
        prisoner.blitme(settingsP[x],grounds)
    
    if settings.game_active:
        settings.score += 1
    text.update_score(settings,screen)
    top.blitme()
    