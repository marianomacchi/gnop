#!/bin/python3

# TODO:
# 1) organize code of main() in more functions and clean thoroughly the code
# 2) use pygame fonts and text to keep scorings
# 3) add sound

import pygame
from random import choice, randint

class Colors:
    black = (0 , 0, 0) # RGB
    white = (255 , 255, 255)

class Display:
    width = 450 # 4:3 ratio
    height = 350
    center = (width//2, height//2)
    # paddles' starting coordinates
    left_paddle_y = (int)(height * 0.45)
    left_paddle_x = (int)(width * 0.10)
    right_paddle_y = (int)(height * 0.45)
    right_paddle_x = (int)(width * 0.90)
    # ball starting coordinates
    ball_x = center[0]
    ball_y = randint(0, height)

class Paddle:
    height = 27
    width = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # a paddle is formed by five, contiguous, rectangles to allow
        # for different resulting angles when hitting the ball
        top = pygame.Rect(self.x, self.y-2*(Paddle.height//5),
                          Paddle.width, Paddle.height//5)
        middletop = pygame.Rect(self.x, self.y-(Paddle.height//5),
                                Paddle.width, Paddle.height//5)
        middle = pygame.Rect(self.x, self.y,  Paddle.width, Paddle.height//5)
        middlebottom = pygame.Rect(self.x, self.y+(Paddle.height//5),
                                   Paddle.width, Paddle.height//5)
        bottom = pygame.Rect(self.x, self.y+2*(Paddle.height//5),
                             Paddle.width, Paddle.height//5)
        self.rectlist = [top, middletop, middle, middlebottom, bottom]
    def move_up(self):
        if self.rectlist[0].top > 20: # the paddles cannot reach the top
            self.rectlist[0].move_ip(0, -5)
            self.rectlist[1].move_ip(0, -5)
            self.rectlist[2].move_ip(0, -5)
            self.rectlist[3].move_ip(0, -5)
            self.rectlist[4].move_ip(0, -5)
    def move_down(self):
        if self.rectlist[4].bottom < Display.height-20: # nor the bottom
            self.rectlist[0].move_ip(0, 5)
            self.rectlist[1].move_ip(0, 5)
            self.rectlist[2].move_ip(0, 5)
            self.rectlist[3].move_ip(0, 5)
            self.rectlist[4].move_ip(0, 5)

class Ball:
    height = 5
    width = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # ball's rectangle (used for movements and collisions)
        self.rect = pygame.Rect(self.x, self.y, Ball.width, Ball.height)
        # direction[0] represents the x-axis, direction[1] the y-axis
        # at instantiation the ball moves randomly either to the left or to
        # the right, in a straightforward line or with an inclination of 45°
        # values greater than 1 leave a trail in the ball movements
        self.direction = [choice([-3, 3]), randint(-2, 2)]
    def move(self):
        # unless acted upon, the ball keeps its direction
        self.rect.move_ip(self.direction[0], self.direction[1])

def init():
    pygame.init()
    game_display = pygame.display.set_mode((Display.width, Display.height))
    pygame.display.set_caption('gnop') # display title
    game_display_rect = game_display.get_rect() # used for collisions
    return game_display, game_display_rect

def draw_background(game_display):
    game_display.fill(Colors.black)
    # draw central line (line segments are drawn from the top every 13 pixels)
    for y in range(Display.height+1):
        if y%13 == 0:
            pygame.draw.line(game_display, Colors.white, (Display.center[0], y),
                            (Display.center[0], y+5), 2) # thick=1

def draw_gameplay(game_display, LeftPaddle, RightPaddle, Ball):
    # draw paddles and ball (0 fills the rectangles, 1 leaves them empty)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle.rectlist[0], 0)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle.rectlist[1], 0)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle.rectlist[2], 0)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle.rectlist[3], 0)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle.rectlist[4], 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle.rectlist[0], 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle.rectlist[1], 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle.rectlist[2], 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle.rectlist[3], 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle.rectlist[4], 0)
    pygame.draw.rect(game_display, Colors.white, Ball, 0)

def draw_ball(game_display, Ball):
    pygame.draw.rect(game_display, Colors.white, Ball, 0)

def main():
    game_display, game_display_rect = init()
    game_clock = pygame.time.Clock()
    # create paddles
    LeftPaddle = Paddle(Display.left_paddle_x, Display.left_paddle_y)
    RightPaddle = Paddle(Display.right_paddle_x, Display.right_paddle_y)
    # create ball
    MainBall = Ball(Display.ball_x, Display.ball_y)
    # main loop
    playing = False
    quit_signal = False
    while not quit_signal:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_signal = True
        pressed_keys = pygame.key.get_pressed() # list
        # Left paddle movements
        if pressed_keys[pygame.K_w]:
            LeftPaddle.move_up()
        if pressed_keys[pygame.K_s]:
            LeftPaddle.move_down()
        # Right paddle movements
        if pressed_keys[pygame.K_UP]:
            RightPaddle.move_up()
        if pressed_keys[pygame.K_DOWN]:
            RightPaddle.move_down()
        if pressed_keys[pygame.K_RETURN]:
            playing = True
            lplayer_score = 0
            rplayer_score = 0
            rally = 0 # number of exchanges between the players

        if playing and (lplayer_score == 11 or rplayer_score == 11):
            playing = False


        # ball bouncing
        # ball goes slightly into the left and right walls but not trough
        # the top and bottom walls
        if MainBall.rect.left < -15 or MainBall.rect.right > Display.width+15:
            if playing: # a point has been made, create a new ball
                MainBall = Ball(Display.ball_x, Display.ball_y)
                rally = 0
                if MainBall.rect.left < -15:
                    lplayer_score += 1
                else:
                    rplayer_score += 1
            else:
                MainBall.direction[0] = -MainBall.direction[0]
        if MainBall.rect.top < 0 or MainBall.rect.bottom > Display.height:
            MainBall.direction[1] = -MainBall.direction[1]

        # if there's a ball-paddles collition, the x-axis of the ball
        # is always inverted (the ball is sent back from where it came)
        if playing:
            if MainBall.rect.collidelist(LeftPaddle.rectlist) != -1 or \
               MainBall.rect.collidelist(RightPaddle.rectlist) != -1:
                   rally += 1
                   if rally%4 == 0: # every 4 exchanges, ball speed increases
                       if MainBall.direction[0] > 0:
                            MainBall.direction[0] += 1
                       else:
                            MainBall.direction[0] -= 1

                   MainBall.direction[0] = -MainBall.direction[0]

            # Different paddle angles
            # The angles vary from top-bottom (higher angle),
            # middle top-middle bottom (angle between middle and top)
            # and middle (straight response)
            if MainBall.rect.colliderect(LeftPaddle.rectlist[0]) or \
               MainBall.rect.colliderect(RightPaddle.rectlist[0]):
                    MainBall.direction[1] = -2
            elif MainBall.rect.colliderect(LeftPaddle.rectlist[1]) or \
                 MainBall.rect.colliderect(RightPaddle.rectlist[1]):
                    MainBall.direction[1] = -1
            elif MainBall.rect.colliderect(LeftPaddle.rectlist[2]) or \
                 MainBall.rect.colliderect(RightPaddle.rectlist[2]):
                    MainBall.direction[1] = 0
            elif MainBall.rect.colliderect(LeftPaddle.rectlist[3]) or \
                 MainBall.rect.colliderect(RightPaddle.rectlist[3]):
                    MainBall.direction[1] = 1
            elif MainBall.rect.colliderect(LeftPaddle.rectlist[4]) or \
                 MainBall.rect.colliderect(RightPaddle.rectlist[4]):
                     MainBall.direction[1] = 2

        # how to detect bottom - top collision?

        MainBall.move()

        draw_background(game_display)
        if playing:
            draw_gameplay(game_display, LeftPaddle, RightPaddle, MainBall)
        else:
            draw_ball(game_display, MainBall)
        pygame.display.update() # renders the display
        game_clock.tick(60) # FPS
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
