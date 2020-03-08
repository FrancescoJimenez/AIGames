
import pygame

class Settings1():

    def __init__(self):
    
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_colour = (66, 43, 23)
        self.store_n = 0
        self.alpha_value = 0
        self.ground_speed = 4
        self.death_ground_speed = 3
        self.decrease_ground = False
        self.decrease = 2
        
        self.jump_flag = False
        self.jump_add_constant = 4
        self.jump_decrease_constant = 0.1
        self.jump_descent = False
        self.jump_sprint = 4
        self.jump_sprint2 = 2.5
        self.jump_type = False
        self.jump_limit = 150
        
        self.music_timer = 0
        
        self.prisoner_position = 230
        self.prisoner_animation_speed = 10
        
        self.spawn_chance = 200
        self.ob_flag = True
        self.ob_timer = 0
        self.ob_limit = 200
        self.ob_limit_spawn = 200
        self.ob_timer_spawn = 0
        self.ob_number = 3
        self.previous_position = 0
        
        self.ob_flag2 = True
        self.ob_timer2 = 0
        self.ob_limit2 = 300
        self.ob_number2 = 3
        self.previous_position2 = 0
        self.ob_flag_position = False
        
        self.player_ground = False
        

        self.score = 0
        self.diff_score = 0
        self.game_active = True
        
        self.jump_sound = pygame.mixer.Sound('Sounds/jump.wav')
        self.death_sound = pygame.mixer.Sound('Sounds/death.wav')
