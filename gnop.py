#!/bin/python3

# TODO:
# 1) organize code of main() in more functions and clean thoroughly the code
# 2) use pygame fonts and text to keep scorings
# 3) add sound

import sys
import pygame
from random import choice, randint

DISPLAY_WIDTH = 450 # 4:3 Ratio
DISPLAY_HEIGHT = 350
LEFT_PADDLE_Y = int(DISPLAY_HEIGHT * 0.45) # Paddles' starting coordinates
LEFT_PADDLE_X = int(DISPLAY_WIDTH * 0.10)
RIGHT_PADDLE_Y = int(DISPLAY_HEIGHT * 0.45)
RIGHT_PADDLE_X = int(DISPLAY_WIDTH * 0.90)
DISPLAY_CENTER = DISPLAY_WIDTH//2 # Ball starting x-axis position (y-axis is random)
BLACK = (0 , 0, 0) # RGB
WHITE = (255 , 255, 255)

class Paddle:
    height = 27
    width = 5
    returning_angles = {
            0 : -2, # top
            1 : -1, # middletop
            2 : 0, # middle
            3 : 1, # middlebottom
            4 : 2 # bottom
    }
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
        self.score = 0
    def move_up(self):
        if self.rectlist[0].top > 20: # the paddles cannot reach the top
            self.rectlist[0].move_ip(0, -5)
            self.rectlist[1].move_ip(0, -5)
            self.rectlist[2].move_ip(0, -5)
            self.rectlist[3].move_ip(0, -5)
            self.rectlist[4].move_ip(0, -5)
    def move_down(self):
        if self.rectlist[4].bottom < DISPLAY_HEIGHT-20: # nor the bottom
            self.rectlist[0].move_ip(0, 5)
            self.rectlist[1].move_ip(0, 5)
            self.rectlist[2].move_ip(0, 5)
            self.rectlist[3].move_ip(0, 5)
            self.rectlist[4].move_ip(0, 5)

class Ball:
    height = 5
    width = 5
    x = DISPLAY_CENTER
    orientation = {'left' : -4, 'right' : 4}
    def __init__(self, to=None, playing=False):
        self.y = randint(0, DISPLAY_HEIGHT)
        self.rect = pygame.Rect(Ball.x, self.y, Ball.width, Ball.height)
        # direction[0] represents the x-axis, direction[1] the y-axis
        if to:
            self.direction = [Ball.orientation[to]]
        else:
            self.direction = [choice([-4, 4])]
        self.direction.append(randint(-4, 4))
        if not playing:
            while self.direction[1] == 0: # exclude straight lines
                self.direction[1] = randint(-4, 4)
    def move(self):
        # unless acted upon, the ball keeps its direction
        self.rect.move_ip(self.direction[0], self.direction[1])

def init():
    pygame.init()
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('gnop') # display title
    game_display_rect = game_display.get_rect()
    return game_display, game_display_rect

def draw_background(game_display):
    game_display.fill(BLACK)
    # draw central line (line segments are drawn from the top every 13 pixels)
    for y in range(DISPLAY_HEIGHT+1):
        if y%13 == 0:
            pygame.draw.line(game_display, WHITE, (DISPLAY_CENTER, y),
                            (DISPLAY_CENTER, y+5), 2) # thick=1

def draw_gameplay(game_display, LeftPaddle, RightPaddle, Ball):
    # draw paddles and ball (0 fills the rectangles, 1 leaves them empty)
    pygame.draw.rect(game_display, WHITE, LeftPaddle.rectlist[0], 0)
    pygame.draw.rect(game_display, WHITE, LeftPaddle.rectlist[1], 0)
    pygame.draw.rect(game_display, WHITE, LeftPaddle.rectlist[2], 0)
    pygame.draw.rect(game_display, WHITE, LeftPaddle.rectlist[3], 0)
    pygame.draw.rect(game_display, WHITE, LeftPaddle.rectlist[4], 0)
    pygame.draw.rect(game_display, WHITE, RightPaddle.rectlist[0], 0)
    pygame.draw.rect(game_display, WHITE, RightPaddle.rectlist[1], 0)
    pygame.draw.rect(game_display, WHITE, RightPaddle.rectlist[2], 0)
    pygame.draw.rect(game_display, WHITE, RightPaddle.rectlist[3], 0)
    pygame.draw.rect(game_display, WHITE, RightPaddle.rectlist[4], 0)
    pygame.draw.rect(game_display, WHITE, Ball, 0)

def draw_ball(game_display, Ball):
    pygame.draw.rect(game_display, WHITE, Ball, 0)

def main():
    game_display, game_display_rect = init()
    game_clock = pygame.time.Clock()
    # create paddles
    LeftPaddle = Paddle(LEFT_PADDLE_X, LEFT_PADDLE_Y)
    RightPaddle = Paddle(RIGHT_PADDLE_X, RIGHT_PADDLE_Y)
    # create ball
    MainBall = Ball()
    playing = False
    # main loop
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
            LeftPaddle.score = 0
            RightPaddle.score = 0
            rally = 0 # exchanges between the players
            MainBall = Ball()

        draw_background(game_display)

        # ball bouncing
        # The ball goes slightly into the left and right walls but not trough
        # the top and bottom walls
        if MainBall.rect.left < -15 or MainBall.rect.right > DISPLAY_WIDTH+15:
            if playing: # a point has been made, create a new ball
                MainBall = Ball()
                rally = 0
                if MainBall.rect.left < -15:
                    LeftPaddle.score += 1
                else:
                    RightPaddle.score += 1
            else:
                MainBall.direction[0] = -MainBall.direction[0]
        if MainBall.rect.top < 0 or MainBall.rect.bottom > DISPLAY_HEIGHT:
            MainBall.direction[1] = -MainBall.direction[1]

        # if there's a ball-paddle collition, the x-axis of the ball
        # is always inverted (the ball is sent back from where it came)
        if playing:
            # check collisions
            collisions = (MainBall.rect.collidelist(LeftPaddle.rectlist),
                          MainBall.rect.collidelist(RightPaddle.rectlist))
            for rect in collisions:
                if rect != -1:
                   MainBall.direction[0] = -MainBall.direction[0]
                   MainBall.direction[1] = Paddle.returning_angles[rect]
                   rally += 1
                   if rally%3 == 0: # every 3 exchanges, ball speed increases
                       if MainBall.direction[0] > 0:
                            MainBall.direction[0] += 1
                       else:
                            MainBall.direction[0] -= 1
            # check score
            if LeftPaddle.score == 11 or RightPaddle.score  == 11:
                playing = False
            draw_gameplay(game_display, LeftPaddle, RightPaddle, MainBall)
        else:
            draw_ball(game_display, MainBall)
        MainBall.move()
        pygame.display.update() # renders the display
        game_clock.tick(60) # FPS
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
