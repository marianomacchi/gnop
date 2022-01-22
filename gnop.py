#!/bin/python3

"""Loose pong clone (Atari, 1972)

This script implements a loose clone of Atari's original pong.

To run the game simply run the script and then - to start a game - press enter.

    Player 1 moves using the WASD keys
    Player 2 moves using the directional keys

The game ends when one of the players reaches 10 points.

This script requires `pygame` to be installed.
"""

__author__ = "Mariano Macchi"
__license__ = "MIT"
__version__ = "1.0.0"

# TODO:
# 1) Add three additional rectangles and returning angles to the paddles
# 2) Add sound
# 3) Use pygame fonts and text to show scorings
# 4) Move the players' score on a different location player != paddle

from random import choice, randint
from sys import exit

import pygame

# The display's size entails an aspect ratio of 4:3
DISPLAY_WIDTH = 454
DISPLAY_HEIGHT = 262
# Players' paddles starting coordinates
LEFT_PADDLE_X = int(DISPLAY_WIDTH * 0.10)
LEFT_PADDLE_Y = int(DISPLAY_HEIGHT * 0.45)
RIGHT_PADDLE_X = int(DISPLAY_WIDTH * 0.90)
RIGHT_PADDLE_Y = int(DISPLAY_HEIGHT * 0.45)
DISPLAY_CENTER = DISPLAY_WIDTH // 2
BLACK = (0 , 0, 0) # RGB
WHITE = (255 , 255, 255)

class Paddle:
    HEIGHT = 27
    WIDTH = 5
    RETURNING_ANGLES = {
            0 : -2, # top
            1 : -1, # middletop
            2 : 0, # middle
            3 : 1, # middlebottom
            4 : 2 # bottom
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        # A paddle is formed by five, contiguous, rectangles whose coordinates
        # are calculated from the paddle's starting coordinates
        # The use of several rectangles allows for different resulting angles
        # when hitting the ball
        top = pygame.Rect(self.x, self.y - (2 * (Paddle.HEIGHT // 5)),
                          Paddle.WIDTH, Paddle.HEIGHT // 5)
        middletop = pygame.Rect(self.x, self.y - (Paddle.HEIGHT // 5),
                                Paddle.WIDTH, Paddle.HEIGHT // 5)
        middle = pygame.Rect(self.x, self.y,  Paddle.WIDTH, Paddle.HEIGHT // 5)
        middlebottom = pygame.Rect(self.x, self.y + (Paddle.HEIGHT // 5),
                                   Paddle.WIDTH, Paddle.HEIGHT // 5)
        bottom = pygame.Rect(self.x, self.y + (2 * (Paddle.HEIGHT // 5)),
                             Paddle.WIDTH, Paddle.HEIGHT // 5)
        self.rectangles = [top, middletop, middle, middlebottom, bottom]

    # The paddle's movement is limited to mimic the same behaviour on the
    # original game: the paddles cannot reach the top, nor the bottom
    def move_up(self):
        """Move all the paddle's rectangles upwards, in place."""
        if self.rectangles[0].top > 20:
            for rectangle in self.rectangles:
                rectangle.move_ip(0, -5)

    def move_down(self):
        """Move all the paddle's rectangles downwards, in place."""
        if self.rectangles[4].bottom < DISPLAY_HEIGHT - 20:
            for rectangle in self.rectangles:
                rectangle.move_ip(0, 5)

class Ball:
    HEIGHT = 5
    WIDTH = 5
    SPEED = 3 # direction along the x-axis
    MIN_INCLINATION = -7 # direction along the y-axis
    MAX_INCLINATION = 7

    def __init__(self, orientation=None, playing=False):
        self.x = DISPLAY_CENTER
        self.y = randint(0, DISPLAY_HEIGHT)
        self.rect = pygame.Rect(self.x, self.y, Ball.WIDTH, Ball.HEIGHT)
        # The orientation (-1 or 1) indicates whether the ball moves left
        # to right (1) or right to left (-1)
        # During gameplay is set by the players hitting the ball
        # It's also used to determine what direction (x, y) the ball is moving
        if orientation:
            self.direction = [orientation * Ball.SPEED] # x-axis
        else:
            self.direction = [choice([-Ball.SPEED, Ball.SPEED])]
        self.direction.append(randint(Ball.MIN_INCLINATION,
            Ball.MAX_INCLINATION)) # y-axis
        if not playing:
            # Exclude straight lines so the ball can bounce around
            while self.direction[1] == 0:
                self.direction[1] = randint(Ball.MIN_INCLINATION,
                        Ball.MAX_INCLINATION)

    def move(self):
        """Move the ball along its current direction."""
        self.rect.move_ip(self.direction[0], self.direction[1])

    def bounce(self):
        """Make the ball bounce against the screen's 'walls'"""
        if self.rect.left < 0 or self.rect.right > DISPLAY_WIDTH:
                self.direction[0] = -self.direction[0]
        if self.rect.top < 0 or self.rect.bottom > DISPLAY_HEIGHT:
                self.direction[1] = -self.direction[1]

def handle_players_input(pressed_keys, LeftPaddle, RightPaddle):
    # Moves the paddles based on players' input
    if pressed_keys[pygame.K_w]: # Left paddle movements
        LeftPaddle.move_up()
    if pressed_keys[pygame.K_s]:
        LeftPaddle.move_down()
    if pressed_keys[pygame.K_UP]: # Right paddle movements
        RightPaddle.move_up()
    if pressed_keys[pygame.K_DOWN]:
        RightPaddle.move_down()

def handle_collisions(LeftPaddle, RightPaddle, MainBall, rally):
    # Handles the collisions of the Ball with the Paddles and with the Walls
    # If the ball hits either of the two paddles, the number of consecutive
    # exchanges within a point (rally) increases, and so does the ball's speed
    # every 3 consecutive exchanges.
    # If the ball hits either the left or the right side of the screen, a point
    # is made and the rally variable is reset.
    point = False
    # Paddle collision
    collisions = (MainBall.rect.collidelist(LeftPaddle.rectangles),
                  MainBall.rect.collidelist(RightPaddle.rectangles))
    for rect in collisions:
        if rect != -1:
           MainBall.direction[0] = -MainBall.direction[0]
           MainBall.direction[1] = Paddle.RETURNING_ANGLES[rect]
           rally += 1
           if rally%3 == 0: # Every 3 exchanges ball speed increases
               if MainBall.direction[0] > 0:
                    MainBall.direction[0] += 1
               else:
                    MainBall.direction[0] -= 1
    # Wall collision
    if MainBall.rect.left < -15 or MainBall.rect.right > DISPLAY_WIDTH+15:
        point = True
        rally = 0
    if MainBall.rect.top < 0 or MainBall.rect.bottom > DISPLAY_HEIGHT:
        MainBall.direction[1] = -MainBall.direction[1]
    return point, rally

def update_score(MainBall, LeftPaddle, RightPaddle):
    # Updates the players' score when a point is made and returns the
    # ball had when the point was made.
    # TODO: refactor this class and check whether the scoring makes sense:
    # shouldn't it be the contrary? i.e. the score is kept in reverse ?
    if MainBall.rect.left < 0:
        LeftPaddle.score += 1
        ball_orientation = -1 # left
    else:
        RightPaddle.score += 1
        ball_orientation = 1 # right
    return ball_orientation

def draw_background(game_display):
    # Fills the background and draws a central line.
    game_display.fill(BLACK)
    for y in range(DISPLAY_HEIGHT+1):
        # line segments are drawn from the top every 13 pixels
        if y%13 == 0:
            pygame.draw.line(game_display, WHITE, (DISPLAY_CENTER, y),
                            (DISPLAY_CENTER, y+5), 2) # thick=2

def draw_gameplay(game_display, LeftPaddle, RightPaddle, Ball, playing):
    # Draws the paddles and the ball.
    # If a game is not being played, it only draws the ball.
    # 0 fills the rectangles, 1 leaves them empty.
    if playing:
        pygame.draw.rect(game_display, WHITE, LeftPaddle.rectangles[0], 0)
        pygame.draw.rect(game_display, WHITE, LeftPaddle.rectangles[1], 0)
        pygame.draw.rect(game_display, WHITE, LeftPaddle.rectangles[2], 0)
        pygame.draw.rect(game_display, WHITE, LeftPaddle.rectangles[3], 0)
        pygame.draw.rect(game_display, WHITE, LeftPaddle.rectangles[4], 0)
        pygame.draw.rect(game_display, WHITE, RightPaddle.rectangles[0], 0)
        pygame.draw.rect(game_display, WHITE, RightPaddle.rectangles[1], 0)
        pygame.draw.rect(game_display, WHITE, RightPaddle.rectangles[2], 0)
        pygame.draw.rect(game_display, WHITE, RightPaddle.rectangles[3], 0)
        pygame.draw.rect(game_display, WHITE, RightPaddle.rectangles[4], 0)
    pygame.draw.rect(game_display, WHITE, Ball, 0)

def main():
    """Initialize the game and keep track of the gameplay through a loop"""
    pygame.init()
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('gnop') # window title
    game_clock = pygame.time.Clock()
    # Create the paddles and the ball
    LeftPaddle = Paddle(LEFT_PADDLE_X, LEFT_PADDLE_Y)
    RightPaddle = Paddle(RIGHT_PADDLE_X, RIGHT_PADDLE_Y)
    MainBall = Ball()
    # Main loop
    playing = False
    quit_signal = False
    while not quit_signal:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_signal = True
        # Get input
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]: # New game
            playing = True
            LeftPaddle.score = 0
            RightPaddle.score = 0
            rally = 0
            MainBall = Ball()

        if playing:
            handle_players_input(pressed_keys, LeftPaddle, RightPaddle)
            point, rally = handle_collisions(LeftPaddle, RightPaddle, MainBall,
                                             rally)
            if point:
                ball_orientation = update_score(MainBall, LeftPaddle,
                                                RightPaddle)
                rally = 0
                MainBall = Ball(ball_orientation)
            if LeftPaddle.score == 11 or RightPaddle.score  == 11:
                playing = False
        else:
            MainBall.bounce()

        MainBall.move()
        draw_background(game_display)
        draw_gameplay(game_display, LeftPaddle, RightPaddle, MainBall, playing)
        pygame.display.update() # Renders the display
        game_clock.tick(60) # FPS
    pygame.quit()
    exit()

if __name__ == '__main__':
    main()
