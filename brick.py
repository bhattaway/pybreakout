import pygame
import random
import time


# bricks. does what it says on the tin
class Brick:
    def __init__(self, color, x, y, w, h, alive=True, points=10):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.alive = alive
        self.points = points

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)

    def __str__(self):
        return "<Brick color:%s rect:%s alive:%s points:%s>" % \
                    (self.color, self.rect, self.alive, self.points)

    def die(self):
        self.alive = False
