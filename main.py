import pygame
import random
import time
from brick import *
from paddle import *
from ball import *
from game import *

def main():

    pygame.init()
    #logo = pygame.image.load("WoodenBox.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("PyBreakout!")

    screen = pygame.display.set_mode((800,600))

    clk = pygame.time.Clock()
    running = True

    '''
    circs = []
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
    START_SCREEN_STATE = 0
    INIT_LEVEL_STATE = 1
    RESET_BALL_STATE = 2
    WAIT_FOR_LAUNCH_STATE = 3
    GAME_STATE = 4
    GAME_OVER_STATE = 5

    game = Game(level_number=1,
                lives=2,
                score=0,
                state=START_SCREEN_STATE,
                num_bricks=0,
                brick_list=[],
                num_balls=0,
                ball_list=[],
                num_paddles=0,
                paddle_list=[],
                )



    ### PADDLE
    # get control scheme (keys or mouse)
    #display some text TODO


    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    smallfont = pygame.font.SysFont("monospace", 24)
    medfont = pygame.font.SysFont("monospace", 32)
    bigfont = pygame.font.SysFont("monospace", 48)

    color_changer = 0
    dcolor = 1

    rchange = random.randrange(256)
    dred = random.randrange(1,9)
    gchange = random.randrange(256)
    dgreen = random.randrange(1,9)
    bchange = random.randrange(256)
    dblue = random.randrange(1,9)

    while running:
        if game.state == START_SCREEN_STATE:
            welcometext = bigfont.render("Welcome to PyBreakout!", 1, (bchange, rchange, gchange))
            instructions = medfont.render("The paddle follows your mouse!", 1, (255,255,255))
            moreinstructions = smallfont.render("Goal: Break all the bricks.", 1, (255,255,255))
            escinstructions = smallfont.render("Press escape at any time to quit.", 1, (200,200,200))
            clicktext = bigfont.render("Click to start!", 1, (rchange,gchange,bchange))
            screen.fill((50,50,50))
            screen.blit(welcometext, (screen.get_width() // 2 - welcometext.get_width() // 2, 50))
            screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, 185))
            screen.blit(moreinstructions, (screen.get_width() // 2 - moreinstructions.get_width() // 2, 300))
            screen.blit(escinstructions, (screen.get_width() // 2 - escinstructions.get_width() // 2, 400))
            screen.blit(clicktext, (screen.get_width() // 2 - clicktext.get_width() // 2, 500))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.state = INIT_LEVEL_STATE

            rchange += dred
            gchange += dgreen
            bchange += dblue

            if rchange > 255:
                rchange = 255
                dred = random.randrange(-9,-3)
            elif rchange < 50:
                rchange = 50
                dred = random.randrange(3,9)
            if gchange > 255:
                gchange = 255
                dgreen = random.randrange(-9,-3)
            elif gchange < 50:
                gchange = 50
                dgreen = random.randrange(3,9)
            if bchange > 255:
                bchange = 255
                dblue = random.randrange(-9,-3)
            elif bchange < 50:
                bchange = 50
                dblue = random.randrange(3,9)

        elif game.state == INIT_LEVEL_STATE:
            screen.fill((50,50,50))
            levelalert = bigfont.render("LEVEL %s" % (game.level_number), 1, (255, 255, 255))
            screen.blit(levelalert, (screen.get_width() // 2 - levelalert.get_width() // 2, \
                                        screen.get_height() // 2 - levelalert.get_height() // 2))
            pygame.display.flip()
            time.sleep(1.5)
            #if no paddle
            if game.num_paddles < 1:
                #load paddle
                p = Mypaddle(color=(230,102,102),
                        x=screen.get_width() / 2,
                        y=screen.get_height() - 55,
                        w=100,
                        h=5,
                        dx=10,
                        dy=5)
                game.add_paddle(p)

            game.clear_bricks()
            #load bricks
            for i in range(5):
                for j in range(8):
                    b = Brick(
                            color=(129,162,225),
                            x=0 + 100*j,
                            y=100 + 41*i,
                            w=99,
                            h=40,
                            points=10,
                            )
                    if random.randrange(10) == 0:
                        b.color = (204,102,102)
                        b.points=100

                    game.add_brick(b)

            game.state = RESET_BALL_STATE



        elif game.state == RESET_BALL_STATE:

            game.clear_balls()
            ball = Mycircle(
                    color=(237,189,95),
                    x=int(screen.get_width() / 2),
                    y=screen.get_height() - 80,
                    r=6,
                    dx=0,
                    dy=0
                    )
            game.add_ball(ball)
            
            game.state = WAIT_FOR_LAUNCH_STATE

        elif game.state == WAIT_FOR_LAUNCH_STATE:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for ball in game.ball_list:
                        ball.dx = 1
                        ball.dy = -6
                    game.state = GAME_STATE

            for p in game.paddle_list:
                p.move(screen)
                for ball in game.ball_list:
                    ball.x = p.rect.x + p.rect.w // 2
                    ball.y = p.rect.y - ball.r - 1

            launchinstructions = smallfont.render("Click to launch the ball!", 1, \
                                (155+color_changer,155+color_changer,155+color_changer))
        
            livestext = smallfont.render("Lives: %s" % (game.lives), 1, (138,190,183))
            leveltext = smallfont.render("Level: %s" % (game.level_number), 1, (181,183,104))
            scoretext = smallfont.render("Score: %s" % (game.score), 1, (223,142,86))
            screen.fill((50,50,50))
            screen.blit(launchinstructions, (screen.get_width() // 2 - launchinstructions.get_width() // 2, \
                            screen.get_height() - 110))
            screen.blit(livestext, (10, screen.get_height() - livestext.get_height() - 7))
            screen.blit(leveltext, (screen.get_width() // 2 - leveltext.get_width() // 2, \
                                screen.get_height() - leveltext.get_height() - 7))
            screen.blit(scoretext, (screen.get_width() - scoretext.get_width() - 10, \
                                screen.get_height() - scoretext.get_height() - 7))

            color_changer += dcolor

            if color_changer > 100:
                color_changer = 100
                dcolor = -2
            elif color_changer < 0:
                dcolor = 2

            #draw
            screen.lock()


            for b in game.brick_list:
                b.draw(screen)
                #print(b)

            for c in game.ball_list:
                c.draw(screen)
                #print(c)

            for p in game.paddle_list:
                p.draw(screen)

            pygame.display.flip()

            screen.unlock()


        elif game.state == GAME_STATE:

            if game.num_bricks < 1:
                game.level_number += 1
                game.state = INIT_LEVEL_STATE

            if game.num_balls < 1:
                game.lives -= 1
                if game.lives < 0:
                    game.state = GAME_OVER_STATE
                else:
                    game.state = RESET_BALL_STATE



            #print stuff
            #move


            for c in game.ball_list:
                c.move(screen)

            for p in game.paddle_list:
                p.move(screen)


            #check collision
            for c in game.ball_list:
                for b in game.brick_list:
                    if c.check_collision_with_brick(b):
                        c.handle_collision_with_brick(b)
                        game.score += b.points

                for p in game.paddle_list:
                    if c.check_collision_with_brick(p):
                        p.handle_collision_with_ball(c)

            game.update_num_bricks()
            game.update_num_balls()
            game.update_num_paddles()


            livestext = smallfont.render("Lives: %s" % (game.lives), 1, (138,190,183))
            leveltext = smallfont.render("Level: %s" % (game.level_number), 1, (181,183,104))
            scoretext = smallfont.render("Score: %s" % (game.score), 1, (223,142,86))
            screen.fill((50,50,50))
            screen.blit(livestext, (10, screen.get_height() - livestext.get_height() - 7))
            screen.blit(leveltext, (screen.get_width() // 2 - leveltext.get_width() // 2, \
                                screen.get_height() - leveltext.get_height() - 7))
            screen.blit(scoretext, (screen.get_width() - scoretext.get_width() - 10, \
                                screen.get_height() - scoretext.get_height() - 7))
            #draw
            screen.lock()


            for b in game.brick_list:
                b.draw(screen)
                #print(b)

            for c in game.ball_list:
                c.draw(screen)
                #print(c)

            for p in game.paddle_list:
                p.draw(screen)

            pygame.display.flip()

            screen.unlock()

        elif game.state == GAME_OVER_STATE:
            #game over!
            #score:
            #click to start a new game
            #press esc to quit
            gameovertext = bigfont.render("GAME OVER!", 1, (rchange,26,26))
            scoretext = bigfont.render("Score: %s" % (game.score), 1, (255,255,255))
            leveltext = medfont.render("Level: %s" % (game.level_number), 1, (255,255,255))
            instructions = smallfont.render("Click to play again!", 1, (255,255,255))
            escinstructions = smallfont.render("Press escape to quit.", 1, (255,255,255))
            screen.fill((50,50,50))
            screen.blit(gameovertext, (screen.get_width() // 2 - gameovertext.get_width() // 2, 100))
            screen.blit(scoretext, (screen.get_width() // 2 - scoretext.get_width() // 2, 200))
            screen.blit(leveltext, (screen.get_width() // 2 - leveltext.get_width() // 2, 300))
            screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, 400))
            screen.blit(escinstructions, (screen.get_width() // 2 - escinstructions.get_width() // 2, 500))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.lives = 2
                    game.score = 0
                    game.level_number = 1
                    game.state = INIT_LEVEL_STATE
            pygame.display.flip()

            rchange += dred

            if rchange > 255:
                rchange = 255
                dred = -2
            elif rchange < 150:
                dred = 2


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
    random.seed(3)
    main()
