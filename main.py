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
    def __init__(self, color, x, y, r, dx, dy, id=0, alive=True):
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.alive = alive
        self.id = id

    def move(self, surface):
        if self.alive:
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
            crect = pygame.Rect(self.x - self.r,
                                self.y - self.r,
                                self.r * 2,
                                self.r * 2)

            return crect.colliderect(b.rect)
        else:
            return False

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

            #input()

        print("AFTER:",self)
        b.die()

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


    def die(self):
        self.alive = False




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

class Game:
    def __init__(self, level_number, num_bricks, brick_list, num_balls, ball_list):
        self.level_number = level_number
        self.num_bricks = num_bricks
        self.brick_list = brick_list
        self.num_balls = num_balls
        self.ball_list = ball_list

    def add_brick(self, brick):
        self.brick_list.append(brick)
        self.update_num_bricks()

    def update_num_bricks(self):
        new_num_bricks = 0
        for brick in self.brick_list:
            if brick.alive:
                new_num_bricks += 1
            
        self.num_bricks = new_num_bricks

    def add_ball(self, ball):
        self.ball_list.append(ball)
        self.update_num_balls()

    def update_num_balls(self):
        new_num_balls = 0
        for ball in self.ball_list:
            if ball.alive:
                new_num_balls += 1
        self.num_balls = new_num_balls



def main():

    pygame.init()
    #logo = pygame.image.load("WoodenBox.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("test minimal program")

    screen = pygame.display.set_mode((700,800))

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
    '''
    for i in range(10):
        c = Mycircle((0,0,i*20),
                random.randrange(screen.get_width()),
                random.randrange(screen.get_height()),
                #random.randrange(20,30),
                5,
                random.randrange(1,6),
                random.randrange(1,6),
                id=i
                )
        #if i == 2:
        circs.append(c)
    '''

    '''
    #use rand seed 12 (probably doesnt matter tho) with test brick
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
    '''
    #test brick
    b = Brick(red, 100, 150, 300, 200)
    bricks.append(b)
    '''



    ### MAKING A LEVEL
    game = Game(level_number=1,
                num_bricks=0,
                brick_list=[],
                num_balls=0,
                ball_list=[],
                )



    ### ACTUAL BRICKS






    ### PADDLE
    # get control scheme (keys or mouse)
    #display some text TODO
    p = Mypaddle(color=green,
            x=screen.get_width() / 2,
            y=screen.get_height() - 20,
            w=100,
            h=5,
            dx=10,
            dy=5)


    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    while running:
        #print stuff
        #move

        for c in game.ball_list:
            c.move(screen)

        p.move(screen)

        #check collision
        for c in game.ball_list:
            for b in game.brick_list:
                if c.check_collision_with_brick(b):
                    c.handle_collision_with_brick(b)

            if c.check_collision_with_brick(p):
                p.handle_collision_with_ball(c)

        game.update_num_bricks()
        game.update_num_balls()

        #if no ball
        if game.num_balls < 1:
            #load ball
            ball = Mycircle(blue,
                    x=int(screen.get_width() / 2),
                    y=screen.get_height() - 100,
                    r=6,
                    dx=5,
                    dy=-10
                    )

            game.add_ball(ball)



        #if no bricks
        if game.num_bricks < 1:
            #load level
            for i in range(4):
                for j in range(5):
                    b = Brick(red,
                            30 + 101*j,
                            20 + 31*i,
                            100,
                            30,
                            )
                    game.add_brick(b)



        #draw
        screen.lock()

        screen.fill((200,0,200))

        for b in game.brick_list:
            b.draw(screen)
            #print(b)

        for c in game.ball_list:
            c.draw(screen)
            #print(c)

        p.draw(screen)

        pygame.display.flip()

        screen.unlock()



        #quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #run at 60 frames per second
        clk.tick(60)
        #input()


if __name__ == "__main__":
    random.seed(int(input()))
    main()
