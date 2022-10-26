import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import math


#reset
#reward
#play(action) -> direction
#game_iteration
#danger




pygame.init()
font_small = pygame.font.SysFont('Lucida Sans',25)

WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)


class Direction(Enum):
    NONE = 1
    RIGHT = 2
    LEFT = 3
    JUMP = 4

Point = namedtuple('Point','x,y')

CHAR_SIZE = 29
MAX_PLATFORMS = 10
aux = 0
GRAVITY = 0.2
SCROLL_TRESH = 200

        








class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,n):
        super().__init__()
        self.image_platform = pygame.image.load("assets/platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_platform, (70, 20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = n
    
    


    def update(self,scroll):

        self.rect.y += scroll

        if self.rect.top > 800:
            self.kill()


    

class JumpGameAI:

    def __init__(self,w=600,h=800):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        self.bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()
        pygame.display.set_caption('Jump')
        self.clock = pygame.time.Clock()
        self.reset()
        self.animation_loop = 1
        self.sheet = pygame.image.load("assets/walk.png").convert_alpha()
        self.flip = False
        
        
        
        
    def reset(self):

        self.char = Point(self.w // 2 - 50, self.h - 80)
        self.speed = 0
        self.direction = Direction.NONE
        self.vel_y = 0
        self.jump = False
        self.numberplat = 0
        self._place_platform()
        self.score = 0
        self.frame_iteration = 0
        self.aux_x = 0
        self.aux_y = 0
        self.coord = Point(0,0)
        self.distanceplatform = 0

# estados    
    def danger(self):
        danger=True
        self.coordplatlist = []
        for i in self.platforms:
            if self.char.y < i.rect.y:
                x = self.coord.x
                y = self.coord.y 
                x = i.rect.x
                y = i.rect.x + 70
                self.coord = Point(x,y)
                self.coordplatlist.append(self.coord)
                

        for pt in self.coordplatlist:
            danger=True
            if self.char.x + CHAR_SIZE > pt.x and self.char.x < pt.y:
                danger = False
                return danger
        
        return danger
    def next_plat(self):
        y = self.char.y
        for platform in self.platforms:
            if y > platform.rect.y and ( self.vel_y ==0.2 or self.vel_y == 0):
                print(y, platform.rect.y)
                self.aux_x = platform.rect.x
                self.aux_y = platform.rect.y
                self.distanceplatform = self.char.x - platform.rect.x

                return self.distanceplatform


        self.distanceplatform = self.char.x - self.aux_x
        return self.distanceplatform
    def next_plat_is_right(self):
        if self.distanceplatform <-15:
            return True
        else:
            return False
    def next_plat_is_left(self):
        if self.distanceplatform > 65:

            return True
        else:
            return False
    def next_plat_is_above(self):
        if self.distanceplatform <= 65 and self.distanceplatform >= -15:
            return True
        else:
            return False
    def going_up(self):
        if self.vel_y < 0:
            return True
        else: 
            return False
    def can_jump(self):
        if self.vel_y ==0.2 or self.vel_y == 0:
            return True
        else:
            return False
    def is_below(self):
        if self.char.y < self.aux_y:
            return True
        else:
            return False

    
        
#juego

    def _place_platform(self):
        self.platforms = pygame.sprite.Group()
        self.platform = Platform(self.w // 2 - 70, self.h - 50, self.numberplat)
        self.platforms.add(self.platform) 

        





    def play_step(self,action):
        self.next_plat()
        self.frame_iteration += 1
        game_over = False
        x = self.char.x
        y = self.char.y
        #1collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  
    

        reward = 0
        if self.next_plat_is_above() and np.array_equal(action,[0,0,1]):
            reward = 8
        
            if self.going_up():
                reward = 10
        if np.array_equal(action,[0,1,0]) and self.next_plat_is_left():
            if self.going_up():
                reward = 10
        if self.is_below() and not self.going_up():
            if np.array_equal(action,[1,0,0]) and self.next_plat_is_right():
                reward = 10
            if np.array_equal(action,[0,1,0]) and self.next_plat_is_left():
                reward = 10
        
        if not self.can_jump() and np.array_equal(action,[0,0,1]):
            reward = -10
        if self.next_plat_is_left() and np.array_equal(action,[1,0,0]):
            reward = -10
        if self.next_plat_is_right() and np.array_equal(action,[0,1,0]):
            reward =-10


        #2.move
        score_before = self.score  #before move

        self._move(action)
        


        score_after = self.score #after move


        if score_after > score_before:
            reward = 10




    
    


        #3.check if game over
        if self.char.y > self.h or self.frame_iteration > (self.score+1)*500:
            reward = -10   
            game_over = True

        #4.place new platform or just move

        if len(self.platforms) < MAX_PLATFORMS:
            self.numberplat += 1
            p_x = random.randint(100,self.w-150)
            p_y = self.platform.rect.y - random.randint(80,120)
            self.platform = Platform(p_x,p_y,self.numberplat)
            self.platforms.add(self.platform) 
        

        

        #update ui and clock
        self._update_ui()
        self.clock.tick(60)


        #6.return game over and score
        return reward, game_over, self.score




    def _update_ui(self):

        
        self.display.blit(self.bg_image,(0,0))
        
        self.platforms.draw(self.display)
        self.platforms.update(self.scroll)
        self.display.blit(self._draw(), (self.char.x,self.char.y))
        #pygame.draw.rect(self.display,RED,pygame.Rect(self.char.x,self.char.y,CHAR_SIZE,CHAR_SIZE) )
        
        text = font_small.render("Score:" + str(self.score), True, WHITE)
        self.display.blit (text,[0,0])

        pygame.display.flip()


    def get_image(self):
        self.image = pygame.Surface((29, 29)).convert_alpha()
        self.image.blit(self.sheet, (0, 0), ((math.floor(self.animation_loop) * 29), 0, 29, 29))
        self.image = pygame.transform.scale(self.image, (29 * 2, 29 * 2))
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey(WHITE)

        return self.image 

    #(self, sheet, frame, width, height, scale)
    def _draw(self):
        
        self.image = self.get_image()
        self.animation_loop += 0.1
        if self.animation_loop >= 8:
            self.animation_loop = 1
        return self.image




    def _move(self, action):
        self.scroll = 0
        x = self.char.x
        y = self.char.y


        if np.array_equal(action,[1,0,0]):
            new_dir = Direction.RIGHT
            self.flip = False
        elif np.array_equal(action,[0,1,0]):
            new_dir = Direction.LEFT
            self.flip = True
        else: #[0,0,1]
            new_dir = Direction.JUMP

        self.direction = new_dir


        if self.direction == Direction.LEFT:
            x = x-5
        elif self.direction == Direction.RIGHT:
            x = x+5


        #check colission with ground
        # if self.char.y + CHAR_SIZE + 2 > self.h: 
        #     y = self.h - CHAR_SIZE
        #     self.vel_y = 0

        if self.direction == Direction.JUMP and (self.vel_y ==0.2 or self.vel_y == 0) :
            self.vel_y = -8

        for platform in self.platforms:
            if platform.rect.colliderect((self.char.x +20) ,(self.char.y + self.vel_y + 45), 20,25):
                 #add new score
                if self.score < platform.number:
                    self.score = platform.number
                 #check if above platform 
                if self.char.y < platform.rect.centery:
                     if self.vel_y > 0:
                        y = platform.rect.top - CHAR_SIZE -25
                        self.vel_y = 0
        if self.vel_y < 5:
            self.vel_y += GRAVITY


        #check if scroll 

        if self.char.y <= SCROLL_TRESH and self.vel_y < 0:
            self.scroll = -self.vel_y 

        self.char = Point(x,y+self.vel_y+self.scroll)






