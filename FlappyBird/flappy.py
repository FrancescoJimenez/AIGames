import pygame
import neat
import time
import os
import random
pygame.font.init()
pygame.init()
x = 400
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
WIN_WIDTH = 450
WIN_HEIGHT = 610
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

pass_sound = pygame.mixer.Sound('sounds/pass.wav')

GEN = 0

BIRD_IMGS = [pygame.image.load("assets/bird1.png"),pygame.image.load("assets/bird2.png"),pygame.image.load("assets/bird3.png")]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("assets/pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("assets/base.png").convert_alpha())
BG_IMG = pygame.image.load("assets/bg.png").convert_alpha()
STAT_FONT = pygame.font.SysFont("comicsans",50)
STAT_FONT2 = pygame.font.SysFont("comicsans",35)


class Base():
    Vel = 5
    Width = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self,y):
        self.y = y 
        self.x1 = 0
        self.x2 = self.Width
        
    def move(self):
        self.x1 -= self.Vel
        self.x2 -= self.Vel
        
        if self.x1 + self.Width < 0:
            self.x1 = self.x2 + self.Width
            
        if self.x2 + self.Width < 0:
            self.x2 = self.x1 + self.Width
    
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
        
class Bird():
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if d >= 11:
            d = 11
            
        if d < 0:
            d -= 2
        
        self.y = self.y + d
        
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
        
    def draw(self,win):
        self.img_count += 1
            
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe():
    Gap = 150
    Vel = 5
    
    def __init__(self,x):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(PIPE_IMG,False,True)
        self.pipe_bottom = PIPE_IMG
        
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50,300)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.Gap
        
    def move(self,Velocity):
        self.x -= Velocity
    
    def draw(self,win):
        win.blit(self.pipe_top,(self.x,self.top))
        win.blit(self.pipe_bottom, (self.x,self.bottom))
    
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        
        return False
        
def draw_window(win,birds,pipes,base,score,gen,pipe_ind):

    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
      
    base.draw(win)
    
    for bird in birds:       
        pygame.draw.line(win, (255,0,0), (bird.x + bird.img.get_width()/2,bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x, pipes[pipe_ind].height),2)
        pygame.draw.line(win, (255,0,0), (bird.x + bird.img.get_width()/2,bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x, pipes[pipe_ind].bottom),2)
        bird.draw(win)
        
    text = STAT_FONT.render("Score: " + str(score), 1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))
    
    text2 = STAT_FONT.render("Gen: " + str(gen), 1,(255,255,255))
    win.blit(text2,(7,10)) 

    text3 = STAT_FONT2.render("Birds: " + str(len(birds)), 1,(0,255,255))
    win.blit(text3,(7,10 + text2.get_height())) 
        
    pygame.display.update()
        
def main(genomes,config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = [] 
    
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(130,250))
        g.fitness = 0
        ge.append(g)
        
    base = Base(530)
    pipes = [Pipe(460)]
    run = True
    score = 0
    diff_score = 0
    Velocity = 5
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_SPACE:
                    bird.jump()
                    
        pipe_ind = 0
        if len(birds)>0:
            if len(pipes)>1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            run = False
            break
                
        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            
            output = nets[x].activate((bird.y,abs(bird.y - pipes[pipe_ind].height),abs(bird.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5:
                bird.jump()
            
            
        add_pipe = False       
        rem = []
        
        if diff_score >= 5:
            Velocity += 2
            base.Vel += 2 
            diff_score = 0
            
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
          
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                    
            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)   
                
            pipe.move(Velocity)
            
        if add_pipe:
            score += 1
            pygame.mixer.Sound.set_volume(pass_sound,0.2)
            pass_sound.play()
            diff_score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))
        
        for r in rem:
            pipes.remove(r)
            pipe_ind = 0
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 510 or bird.y < 0:
               birds.pop(x)
               nets.pop(x)
               ge.pop(x)
                
        base.move()
        draw_window(win,birds,pipes,base,score,GEN,pipe_ind)
        

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main,50)
    
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"Config.txt")
    run(config_path)
    
    
    
    
    
    
        