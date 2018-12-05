import pygame
import random

blue = (0,0,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)

'''
class Mycircle2(pygame.sprite.Sprite):
    def __init__(self, color
'''
class Mypuck:
    def __init__(self, color, x, y, w, h, dx, dy):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.dx = dx
        self.dy = dy
    def __init__(self, color, x, y, w, h, alive=True):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.alive = alive

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)

    def __str__(self):
        return "<Brick color:%s rect:%s alive:%s>" % \
                    (self.color, self.rect, self.alive)


class Mycircle:
    def __init__(self, color, x, y, r, dx, dy, id=0):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.id = id

    def move(self, surface):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.r < 0:
            self.x = self.r
            self.dx = -self.dx
        if self.x + self.r > surface.get_width():
            self.x = surface.get_width() - self.r
            self.dx = -self.dx
        if self.y - self.r < 0:
            self.y = self.r
            self.dy = -self.dy
        if self.y + self.r > surface.get_height():
            self.y = surface.get_height() - self.r
            self.dy = -self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)

    def __str__(self):
        return "<Circle color:%s x:%s y:%s r:%s dx:%s dy:%s id:%s>" % \
                    (self.color, self.x, self.y, self.r, self.dx, self.dy, self.id)

    def check_collision_with_brick(self, b):
        crect = pygame.Rect(self.x - self.r,
                            self.y - self.r,
                            self.r * 2,
                            self.r * 2)

        return crect.colliderect(b.rect)

    def handle_collision_with_brick(self, b):

        print("BEFORE:",self)
        print("BRICK:",b)

        #self.color = green
        brickleft = abs(b.rect.x - self.x + self.dx)
        if brickleft < self.r:
            print("\t\tCHANGING BRICKLEFT FROM",brickleft)
            brickleft = 999
        brickright = abs(self.x - b.rect.x - b.rect.w - self.dx)
        if brickright < self.r:
            print("\t\tCHANGING BRICKRIGHT FROM",brickright)
            brickright = 999

        xdiff = min(brickleft, brickright)

        brickup = abs(b.rect.y - self.y + self.dy)
        if brickup < self.r:
            print("\t\tCHANGING BRICKUP FROM",brickup)
            brickup = 999
        brickdown = abs(self.y - b.rect.y - b.rect.h - self.dy)
        if brickdown < self.r:
            print("\t\tCHANGING BRICKDOWN FROM",brickdown)
            brickdown = 999
        ydiff = min(brickup, brickdown)

        print("\tbrickleft", brickleft)
        print("\tbrickright", brickright)
        print("\tbrickup", brickup)
        print("\tbrickdown", brickdown)

        #
        if xdiff < ydiff:
            #bounce sideways
            print("\thoriz bounce")
            self.dx = -self.dx
            if brickleft < brickright:
                self.x = b.rect.x - self.r 
            else:
                self.x = b.rect.x + b.rect.w + self.r 
        elif xdiff > ydiff:
            #bounce vertically
            print("\tvert bounce")
            self.dy = -self.dy
            if brickup < brickdown:
                self.y = b.rect.y - self.r 
            else:
                self.y = b.rect.y + b.rect.h + self.r 
        else:
            print("THEY ARE EQUAL WTF DO I DO")
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

            input()

        print("AFTER:",self)

class Brick:
    def __init__(self, color, x, y, w, h, alive=True):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.alive = alive

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)

    def __str__(self):
        return "<Brick color:%s rect:%s alive:%s>" % \
                    (self.color, self.rect, self.alive)


def main():

    pygame.init()
    #logo = pygame.image.load("WoodenBox.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("test minimal program")

    screen = pygame.display.set_mode((700,600))

    clk = pygame.time.Clock()
    running = True

    circs = []
    '''
    for i in range(100):
        c = Mycircle((0,0,i*2), 
                445,
                325+i,
                30,
                -1,
                -1,
                id=i
                )
        circs.append(c)
    '''
    for i in range(10):
        c = Mycircle((0,0,i*20),
                random.randrange(screen.get_width()),
                random.randrange(screen.get_height()),
                #random.randrange(20,30),
                3,
                random.randrange(1,6),
                random.randrange(1,6),
                id=i
                )
        #if i == 2:
        circs.append(c)

    '''
    #use rand seed 12
    cc = Mycircle(black, 
            54,
            327,
            29,
            5,
            -2
            )
    circs.append(cc)
    '''

    bricks = []
    b = Brick(red, 100, 150, 300, 200)
    bricks.append(b)

    while running:
        #print stuff
        #move

        for c in circs:
            c.move(screen)

        #check collision
        for c in circs:
            for b in bricks:
                if c.check_collision_with_brick(b):
                    c.handle_collision_with_brick(b)

        #draw
        screen.lock()

        screen.fill((200,0,200))

        for b in bricks:
            b.draw(screen)
            #print(b)

        for c in circs:
            c.draw(screen)
            #print(c)

        pygame.display.flip()

        screen.unlock()



        #quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #run at 30 frames per second
        clk.tick(30)
        #input()


if __name__ == "__main__":
    random.seed(int(input()))
    main()
