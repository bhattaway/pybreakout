import pygame
import random

blue = (0,0,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)

class Mycircle:
    def __init__(self, color, x, y, r, dx, dy):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy

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
        return "<Circle color:%s x:%s y:%s r:%s dx:%s dy:%s>" % \
                    (self.color, self.x, self.y, self.r, self.dx, self.dy)

    def check_collision_with_brick(self, b):
        crect = pygame.Rect(self.x - self.r,
                            self.y - self.r,
                            self.r * 2,
                            self.r * 2)

        return crect.colliderect(b.rect)

    def handle_collision_with_brick(self, b):
        self.color = green
        brickleft = abs(b.rect.x - self.x)
        brickright = abs(self.x - b.rect.x)

        xdiff = min(brickleft, brickright)

        brickup = abs(b.rect.y - self.y)
        brickdown = abs(self.y - b.rect.y)
        ydiff = min(brickup, brickdown)

        #
        if xdiff < ydiff:
            #bounce sideways
            self.dx = -self.dx
            #if brickleft < brickright:
                #self.x = b.xgit@github.com:bhattaway/pybreakout.git
        else:
            #bounce vertically
            self.dy = -self.dy

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
    for i in range(10):
        c = Mycircle(black, 
                random.randrange(screen.get_width()), 
                random.randrange(screen.get_height()),
                random.randrange(1,30), 
                3,
                3
                )
        circs.append(c)

    cc = Mycircle(black, 
            350,
            175,
            51,
            0,
            0
            )
    circs.append(cc)

    bricks = []
    b = Brick(red, 100, 50, 200, 75)
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
            print(b)

        for c in circs:
            c.draw(screen)
            print(c)

        pygame.display.flip()

        screen.unlock()



        #quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #run at 30 frames per second
        clk.tick(30)


if __name__ == "__main__":
    main()
