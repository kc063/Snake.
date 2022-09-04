import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAgent:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        # init game state
        
    def reset(self):
        self.frames = 0
        self.q = []
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

    def _calc_reward(self):
        if(abs(self.head.x -self.food.x) < 60 and abs(self.head.y - self.food.y) < 60):
            return 3
        elif(abs(self.head.x -self.food.x) < 40 and abs(self.head.y - self.food.y) < 40):
            return 5
        else:
            return 0


        
    def play_step(self, action):
        self.frames += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()        
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frames > 50*len(self.snake):
            game_over = True
            reward = -80
            print(self.frames)
            #print(self.q)
            return reward, game_over, self.score, self.frames
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 30
            self._place_food()
        else:
            self.snake.pop()
            reward = self._calc_reward()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        reward += 1
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
            self.q.append(a) 
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
            a = ['L']
            self.q.append(a) 
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
            a = ['D']
            self.q.append(a) 
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            a = ['U']
            self.q.append(a) 
            
        self.head = Point(x, y)