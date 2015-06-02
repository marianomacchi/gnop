#!/bin/python3

# TODO:
# 1) gameplay
# 2) organize code of main() in more functions
# 3) use pygame fonts and text to keep scorings

import pygame
from random import choice

class Colors:
    black = (0 , 0, 0) # RGB
    white = (255 , 255, 255)

class Display:
    width = 640
    height = 320
    center = (width//2, height//2)
    # paddles' starting coordinates
    left_paddle_y = (int)(height * 0.45)
    left_paddle_x = (int)(width * 0.10)
    right_paddle_y = (int)(height * 0.45)
    right_paddle_x = (int)(width * 0.90)
    # ball starting coordinates
    ball_x = center[0]
    ball_y = center[1]

class Paddle:
    height = 24
    width = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # paddle's rectangle (used for movements and collisions)
        self.rect = pygame.Rect(self.x, self.y, Paddle.width, Paddle.height)
    def move_up(self):
        self.rect.move_ip(0, -1)
    def move_down(self):
        self.rect.move_ip(0, 1)

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
        self.direction = [choice([-1, 1]), choice([-1, 0, 1])]
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
    # draw central line (line segments are drawn from the top every 15 pixels)
    for y in range(Display.height+1):
        if y%15 == 0:
            pygame.draw.line(game_display, Colors.white, (Display.center[0], y),
                            (Display.center[0], y+5), 3) # thick=3

def draw_gameplay(game_display, LeftPaddle, RightPaddle, Ball):
    # draw paddles and ball (0 fills the rectangles, 1 leaves them empty)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle, 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle, 0)
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

        # ball bouncing
        if MainBall.rect.left < 0 or MainBall.rect.right > Display.width:
            MainBall.direction[0] = -MainBall.direction[0]
        if MainBall.rect.top < 0 or MainBall.rect.bottom > Display.height:
            MainBall.direction[1] = -MainBall.direction[1]
        MainBall.move()

        # paddles' - ball collition
        if MainBall.rect.colliderect(RightPaddle.rect):
            MainBall.direction[0] = -MainBall.direction[0]
        if MainBall.rect.colliderect(LeftPaddle.rect):
            MainBall.direction[0] = -MainBall.direction[0]

        # ensure paddles are inside the game display
        LeftPaddle.rect.clamp_ip(game_display_rect)
        RightPaddle.rect.clamp_ip(game_display_rect)

        draw_background(game_display)
        draw_gameplay(game_display, LeftPaddle, RightPaddle, MainBall)
        pygame.display.update() # renders the display
        game_clock.tick(250) # FPS
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
