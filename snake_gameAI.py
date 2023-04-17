from cmath import rect
import sys, time, random, pygame
from turtle import right
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

Point = namedtuple('Point', 'x, y')

#colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

BLOCK_SIZE = 20
SPEED = 15

class SnakeGameAI:
    
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SNAKE')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        #init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]
        self.score = 0
        self.kill_cooldown = 100
        self.food = None
        self.place_food()
        #self.iterations = 0
    
    def place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self, action):
        #self.iterations += 1
        # 1. collect user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self.move(action)
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.collision() or self.kill_cooldown == 0:
            game_over = True
            reward = -1
            return reward, game_over, self.score
        
        # 4. place new food 
        if self.head == self.food:
            self.score += 1
            reward = 1
            self.iterations = 0
            self.place_food()
            self.kill_cooldown = 100 + len(self.snake)
        else:
            self.snake.pop()
            self.kill_cooldown -= 1

        # 5. update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return reward, game_over, self.score

    def collision(self, pt = None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        self.display.fill(BLACK)

        for part in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(part.x + 2, part.y + 2, BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text1 = font.render('SCORE:' + str(self.score), True, WHITE)
        self.display.blit(text1, [0, 0])
        text2 = font.render('KILL COOLDOWN:' + str(self.kill_cooldown), True, WHITE)
        self.display.blit(text2, [0, 20])
        pygame.display.flip()

    def move(self, action):
        clock_directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_directions.index(self.direction)

        if np.array_equal(action, [1, 0, 0]): #no change of direction
            new_direction = clock_directions[index]
        elif np.array_equal(action, [0, 1, 0]): #turn right
            next_index = (index + 1) % 4
            new_direction = clock_directions[next_index]
        else:
            next_index = (index - 1) % 4
            new_direction = clock_directions[next_index]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)