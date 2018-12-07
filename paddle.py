import pygame
import random
import time

class Mypaddle:
    def __init__(self, color, x, y, w, h, dx=1, dy=1, alive=True):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.alive = alive
        self.dx = dx
        self.dy = dy

    def move(self, surface):
        if self.alive:
            '''
            #keyboard movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                #print("pressing a")
                self.rect.x -= self.dx
            if keys[pygame.K_s]:
                #print("pressing s")
                self.rect.x += self.dx
            if keys[pygame.K_d]:
                pass
                #print("pressing d")
            '''
            


            #mouse movement
            mousex, mousey = pygame.mouse.get_pos()

            self.rect.x = mousex - (self.rect.w // 2)



        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.w > surface.get_width():
            self.rect.x = surface.get_width() - self.rect.w


    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)

    def __str__(self):
        return "<Mypaddle color:%s rect:%s alive:%s>" % \
                    (self.color, self.rect, self.alive)

    def die(self):
        print("HAHA paddles cannot die")
        pass

    def handle_collision_with_ball(self, c):

        '''
        print("BEFORE:",self)
        print("BALL:",c)
        '''

        c.dy = -c.dy

        midpaddle = self.rect.x + (self.rect.w // 2)
        size_of_increments = self.rect.w // 10
        c.dx = (c.x - midpaddle) // size_of_increments

