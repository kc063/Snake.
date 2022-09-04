from operator import truediv
import pygame
import random
from collections import deque
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

# THIS IS THE VERSION OF THE GAME WITH CRUMB EATING FUNCTIONALITY 

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class GameMode(Enum):
    STANDARD = 1
    CRUMB = 2
    FEAR = 3
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 50

class SnakeGameAgent:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.t = False
        self.turns = 0
        self.unloopable = deque(maxlen = 10)
        self.GameMode = GameMode.FEAR
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        # init game state
        
    def reset(self):
        self.frames = 0
        #self.turns = 6
        #self.crumbable = True
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        reward = 0
        self.frames += 1
        #trying to stop fuckin looping
        if(self.GameMode == GameMode.FEAR):
            if(self.head in self.unloopable):
                reward -= 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self.is_collision() or self.frames > 100*len(self.snake):
            game_over = True
            reward = -10
            #more debug functionality, this time for checking frames (let me catch the LR bug)
            #print(self.frames)
            return reward, game_over, self.score, self.frames
            
        # 4. place new food or just move
        # and add crumb
        if(self.GameMode == GameMode.FEAR or self.GameMode == GameMode.CRUMB):
            #if(self.crumbable is True):
                reward = self.crumb_distance()
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
            self.crumbable = True
            self.turns = 6
        else:
            self.snake.pop()
            
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score, self.frames
    
    def is_collision(self, pt = None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False

    def crumb_distance(self):
        #if(self.turns == 0):
        #    self.crumbable = False
        rd = 0
        #if(self.crumbable == True):
        if(abs(self.head.x - self.food.x) <= 60 and abs(self.head.y - self.food.y) <= 60):
            rd += .5
            #self.turns -= 1
        if(abs(self.head.x - self.food.x) <= 40 and abs(self.head.y - self.food.y) <= 40):
            rd += 1
        if(abs(self.head.x - self.food.x) <= 20 and abs(self.head.y - self.food.y) <= 20):
            rd += 2
        return rd
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        #[straight, right, left]
        new_dir = Direction.RIGHT
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if(np.array_equal(action, [1,0,0])):
            new_dir = clock_wise[idx]
        if(np.array_equal(action, [0,1,0])):
            next_idex = (idx + 1) % 4
            new_dir = clock_wise[next_idex]
        if(np.array_equal(action, [0, 0,1])):
            next_idex = (idx - 1) % 4
            new_dir = clock_wise[next_idex] 
        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
            a = ['R']
            #self.q.append(a) 
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
            a = ['L']
            #self.q.append(a) 
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
            a = ['D']
            #self.q.append(a) 
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            a = ['U']
            #self.q.append(a)   
        self.head = Point(x, y)
        self.unloopable.append(self.head)