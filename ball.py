#brandon hattaway
import pygame
import random
import time

# the class of the ball/puck

#beware, messy hacky code and strange algebra equations lie in wait.
#this needs to be cleaned up and simplified.

class Mycircle:
    def __init__(self, color, x, y, r, dx, dy, id=0, alive=True):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.alive = alive
        self.id = id

    # moves the ball
    def move(self, surface):
        if self.alive:
            self.x += self.dx
            self.y += self.dy

            # bounce off left/right/top of screen
            if self.x - self.r < 0:
                self.x = self.r
                self.dx = -self.dx
            if self.x + self.r > surface.get_width():
                self.x = surface.get_width() - self.r
                self.dx = -self.dx
            if self.y - self.r < 0:
                self.y = self.r
                self.dy = -self.dy

            '''
            #bounce off bottom of screen
            if self.y + self.r > surface.get_height():
                self.y = surface.get_height() - self.r
                self.dy = -self.dy
            '''

            #die off bottom of screen
            if self.y - self.r > surface.get_height():
                self.alive = False

    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)

    def __str__(self):
        return "<Circle color:%s x:%s y:%s r:%s dx:%s dy:%s id:%s alive:%s>" % \
                    (self.color, self.x, self.y, self.r, self.dx, self.dy, self.id, self.alive)

    def check_collision_with_brick(self, b):
        if self.alive and b.alive:
            #collision check assumes the ball is actually a square.
            #to be changed eventually
            crect = pygame.Rect(self.x - self.r,
                                self.y - self.r,
                                self.r * 2,
                                self.r * 2)

            return crect.colliderect(b.rect)
        else:
            return False

    
    # the most disgusting, messy function i've probably ever written. needs major refactoring.
    # read at your own risk

    #this code basically determines which side of the brick the ball ran into, and how to bounce back.
    def handle_collision_with_brick(self, b):

        #print("BEFORE:",self)
        #print("BRICK:",b)


        #find distance to left/right side of brick
        brickleft = abs(b.rect.x - self.x + self.dx)
        if brickleft < self.r:
            #print("\t\tCHANGING BRICKLEFT FROM",brickleft)
            brickleft = 999
        brickright = abs(self.x - b.rect.x - b.rect.w - self.dx)
        if brickright < self.r:
            #print("\t\tCHANGING BRICKRIGHT FROM",brickright)
            brickright = 999

        xdiff = min(brickleft, brickright)

        #find distance  to top/bottom of brick
        brickup = abs(b.rect.y - self.y + self.dy)
        if brickup < self.r:
            #print("\t\tCHANGING BRICKUP FROM",brickup)
            brickup = 999
        brickdown = abs(self.y - b.rect.y - b.rect.h - self.dy)
        if brickdown < self.r:
            #print("\t\tCHANGING BRICKDOWN FROM",brickdown)
            brickdown = 999
        ydiff = min(brickup, brickdown)

        '''
        print("\tbrickleft", brickleft)
        print("\tbrickright", brickright)
        print("\tbrickup", brickup)
        print("\tbrickdown", brickdown)
        '''

        if xdiff < ydiff:
            #bounce sideways
            #print("\thoriz bounce")
            self.dx = -self.dx
            if brickleft < brickright:
                self.x = b.rect.x - self.r 
            else:
                self.x = b.rect.x + b.rect.w + self.r 
        elif xdiff > ydiff:
            #bounce vertically
            #print("\tvert bounce")
            self.dy = -self.dy
            if brickup < brickdown:
                self.y = b.rect.y - self.r 
            else:
                self.y = b.rect.y + b.rect.h + self.r 
        else:
            #stupidly messy and overcomplicated code
            #print("THEY ARE EQUAL WTF DO I DO")
            test = []
            test.append(abs(b.rect.x - self.r - self.x))
            test.append(abs(self.x - b.rect.x - b.rect.w - self.r))
            test.append(abs(b.rect.y - self.r  - self.y))
            test.append(abs(self.y - b.rect.y - b.rect.h - self.r))

            real = []
            real.append(b.rect.x - self.r)
            real.append(b.rect.x + b.rect.w + self.r)
            real.append(b.rect.y - self.r)
            real.append(b.rect.y + b.rect.h + self.r)

            mini = min(test[0], test[1], test[2], test[3])
            mini = 9999
            minindex = 5
            for i in range(4):
                if mini > test[i]:
                    mini = test[i]
                    minindex = i

            if minindex < 2:
                self.x = real[minindex]
                self.dx = -self.dx
            else:
                self.y = real[minindex]
                self.dy = -self.dy

            #input()

        #print("AFTER:",self)

        #kill the brick
        b.die()

