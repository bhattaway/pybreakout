#brandon hattaway
import pygame
import random
import time

# the class that 'oversees' and 'manages' all the other small stuff
# all the methods do exactly what they say on the tin
# should probably move more code into here
class Game:
    def __init__(self, level_number, lives,
            state, #used to differentiate between start screen, gameplay, game over screen, etc.
            score,
            num_bricks, brick_list, 
            num_balls, ball_list,
            num_paddles, paddle_list,
            ):

        self.level_number = level_number
        self.lives = lives
        self.state = state
        self.score = score
        self.num_bricks = num_bricks
        self.brick_list = brick_list
        self.num_balls = num_balls
        self.ball_list = ball_list
        self.num_paddles = num_paddles
        self.paddle_list = paddle_list

    def add_brick(self, brick):
        self.brick_list.append(brick)
        self.update_num_bricks()

    def update_num_bricks(self):
        new_num_bricks = 0
        for brick in self.brick_list:
            if brick.alive:
                new_num_bricks += 1
            
        self.num_bricks = new_num_bricks

    def clear_bricks(self):
        self.brick_list = []
        self.num_bricks = 0

    def add_ball(self, ball):
        self.ball_list.append(ball)
        self.update_num_balls()

    def update_num_balls(self):
        new_num_balls = 0
        for ball in self.ball_list:
            if ball.alive:
                new_num_balls += 1
        self.num_balls = new_num_balls

    def clear_balls(self):
        self.ball_list = []
        self.num_balls = 0

    def add_paddle(self, paddle):
        self.paddle_list.append(paddle)
        self.update_num_paddles()

    def update_num_paddles(self):
        new_num_paddles = 0
        for paddle in self.paddle_list:
            if paddle.alive:
                new_num_paddles += 1
        self.num_paddles = new_num_paddles

    def clear_paddles(self):
        self.paddle_list = []
        self.num_paddles = 0

