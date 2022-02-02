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
# 1) make the display size a valid parameter e.g. python gnop -s 800 600

from random import choice, randint
from sys import exit

import pygame

# The default display's size entails an aspect ratio of 4:3
DISPLAY_WIDTH = 454
DISPLAY_HEIGHT = 262
# Players' paddles starting coordinates
LEFT_PADDLE_X = int(DISPLAY_WIDTH * 0.10)
LEFT_PADDLE_Y = int(DISPLAY_HEIGHT * 0.45)
RIGHT_PADDLE_X = int(DISPLAY_WIDTH * 0.90)
RIGHT_PADDLE_Y = int(DISPLAY_HEIGHT * 0.45)
# Game display defaults
DISPLAY_CENTER = DISPLAY_WIDTH // 2
BLACK = (0, 0, 0)  # RGB
WHITE = (255, 255, 255)
CENTRAL_LINE_THICKNESS = 2
LINE_SEGMENT_LENGTH = 13
FONT_SIZE = DISPLAY_HEIGHT // 10
# Gameplay defaults
MAX_SCORE = 10
LEFT_SIDE_WALL = 1  # Flag
RIGHT_SIDE_WALL = 2
RALLY_SPEEDUP = 5


class Paddle:
    HEIGHT = DISPLAY_HEIGHT // 8
    WIDTH = DISPLAY_WIDTH // 100
    RETURNING_ANGLES = {
        0: -2,  # top
        1: -1,  # middletop
        2: 0,  # middle
        3: 1,  # middlebottom
        4: 2,  # bottom
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        # A paddle is formed by five, contiguous, rectangles whose coordinates
        # are calculated from the paddle's starting coordinates
        # The use of several rectangles allows for different resulting angles
        # when hitting the ball
        top = pygame.Rect(
            self.x,
            self.y - (2 * (Paddle.HEIGHT // 5)),
            Paddle.WIDTH,
            Paddle.HEIGHT // 5,
        )
        middletop = pygame.Rect(
            self.x, self.y - (Paddle.HEIGHT // 5), Paddle.WIDTH, Paddle.HEIGHT // 5
        )
        middle = pygame.Rect(self.x, self.y, Paddle.WIDTH, Paddle.HEIGHT // 5)
        middlebottom = pygame.Rect(
            self.x, self.y + (Paddle.HEIGHT // 5), Paddle.WIDTH, Paddle.HEIGHT // 5
        )
        bottom = pygame.Rect(
            self.x,
            self.y + (2 * (Paddle.HEIGHT // 5)),
            Paddle.WIDTH,
            Paddle.HEIGHT // 5,
        )
        self.rectangles = [top, middletop, middle, middlebottom, bottom]

    # The paddle's movement is limited to mimic the same behaviour on the
    # original game: the paddles cannot reach the top, nor the bottom
    def move_up(self):
        """Move all the paddle's rectangles upwards, in place."""
        if self.rectangles[0].top > DISPLAY_HEIGHT // 20:
            for rectangle in self.rectangles:
                rectangle.move_ip(0, -DISPLAY_HEIGHT // 50)

    def move_down(self):
        """Move all the paddle's rectangles downwards, in place."""
        if self.rectangles[4].bottom < DISPLAY_HEIGHT - DISPLAY_HEIGHT // 20:
            for rectangle in self.rectangles:
                rectangle.move_ip(0, DISPLAY_HEIGHT // 50)


class Ball:
    HEIGHT = DISPLAY_HEIGHT // 50
    WIDTH = DISPLAY_HEIGHT // 50
    SPEED = DISPLAY_WIDTH // 150  # direction along the x-axis
    MIN_INCLINATION = Paddle.RETURNING_ANGLES[0]  # direction along the y-axis
    MAX_INCLINATION = Paddle.RETURNING_ANGLES[4]

    def __init__(self, orientation=None, playing=False):
        self.x = DISPLAY_CENTER
        self.y = randint(0, DISPLAY_HEIGHT)
        self.rect = pygame.Rect(self.x, self.y, Ball.WIDTH, Ball.HEIGHT)
        # The orientation (-1 or 1) indicates whether the ball moves left
        # to right (1) or right to left (-1)
        # During gameplay is set by the players hitting the ball
        # It's also used to determine what direction (x, y) the ball is moving
        if orientation:
            self.direction = [orientation * Ball.SPEED]  # x-axis
        else:
            self.direction = [choice([-Ball.SPEED, Ball.SPEED])]
        self.direction.append(
            randint(Ball.MIN_INCLINATION, Ball.MAX_INCLINATION)
        )  # y-axis
        if not playing:
            # Exclude straight lines so the ball can bounce around
            while self.direction[1] == 0:
                self.direction[1] = randint(Ball.MIN_INCLINATION, Ball.MAX_INCLINATION)

    def move(self):
        """Move the ball along its current direction."""
        self.rect.move_ip(self.direction[0], self.direction[1])

    def bounce_around(self):
        """Make the ball bounce around against the screen's 'walls'"""
        if self.rect.left < 0 or self.rect.right > DISPLAY_WIDTH:
            self.direction[0] = -self.direction[0]
        if self.rect.top < 0 or self.rect.bottom > DISPLAY_HEIGHT:
            self.direction[1] = -self.direction[1]

    def bounce_from_paddle(self, left_paddle, right_paddle, rally):
        """Make the ball bounce from the paddles"""
        paddle_collisions = (
            self.rect.collidelist(left_paddle.rectangles),
            self.rect.collidelist(right_paddle.rectangles),
        )
        for rect in paddle_collisions:
            if rect != -1:
                pygame.mixer.music.load("beep-02.wav")
                pygame.mixer.music.play()
                self.direction[0] = -self.direction[0]
                self.direction[1] = Paddle.RETURNING_ANGLES[rect]
                rally += 1
                if (
                    rally % RALLY_SPEEDUP == 0
                ):  # Ball speed increases when the number of exchanges
                    self.increase_speed()
        return rally

    def bounce_from_walls(self):
        """Make the ball bounce around against the screen's 'walls'
        Return a flag to indicate if and which of the side 'walls' was hit
        """
        side_wall_hit = None
        if self.rect.left < 0 or self.rect.right > DISPLAY_WIDTH:
            self.direction[0] = -self.direction[0]
            if self.rect.left < 0:
                side_wall_hit = LEFT_SIDE_WALL
            else:
                side_wall_hit = RIGHT_SIDE_WALL
        elif self.rect.top < 0 or self.rect.bottom > DISPLAY_HEIGHT:
            self.direction[1] = -self.direction[1]
        return side_wall_hit

    def handle_collisions(self, left_paddle, right_paddle, rally):
        """Handle the ball collisions againts the paddles and the 'walls'"""
        side_wall_hit = self.bounce_from_walls()
        rally = self.bounce_from_paddle(left_paddle, right_paddle, rally)
        return side_wall_hit, rally

    def increase_speed(self):
        """Increase the ball's speed along its current direction"""
        if self.direction[0] > 0:
            self.direction[0] += self.SPEED // 2
        else:
            self.direction[0] -= self.SPEED // 2


def handle_players_input(pressed_keys, left_paddle, right_paddle):
    """Move the paddle according to players' input"""
    if pressed_keys[pygame.K_w]:  # Left paddle movements
        left_paddle.move_up()
    if pressed_keys[pygame.K_s]:
        left_paddle.move_down()
    if pressed_keys[pygame.K_UP]:  # Right paddle movements
        right_paddle.move_up()
    if pressed_keys[pygame.K_DOWN]:
        right_paddle.move_down()


def update_score(side_wall_hit, left_paddle, right_paddle):
    """Update the current players' score after a point is made"""
    if side_wall_hit == LEFT_SIDE_WALL:
        right_paddle.score += 1
    elif side_wall_hit == RIGHT_SIDE_WALL:
        left_paddle.score += 1


def get_after_point_orientation(ball):
    """Return a new orientation after one of the players score"""
    # The new orientation is towards the player that was scored upon
    # The new orientation can be either be -1 or 1 where
    # -1 = right to left
    #  1 = left to right
    ball_orientation = -1 if ball.rect.left < 0 else 1
    return ball_orientation


def draw_background(game_display):
    """Draw the black background and the central white line"""
    game_display.fill(BLACK)
    for y in range(DISPLAY_HEIGHT + 1):
        # line segments are drawn from the top according a fixed length
        if y % LINE_SEGMENT_LENGTH == 0:
            pygame.draw.line(
                game_display,
                WHITE,
                (DISPLAY_CENTER, y),
                (DISPLAY_CENTER, y + 5),
                CENTRAL_LINE_THICKNESS,
            )


def draw_gameplay(game_display, left_paddle, right_paddle, ball, playing):
    """Draw the paddles and the ball"""
    # If a game is not being played, it only draws the ball bouncing
    # 0 fills the rectangles, 1 leaves them empty
    if playing:
        for left_paddle_rectangle in left_paddle.rectangles:
            pygame.draw.rect(game_display, WHITE, left_paddle_rectangle, 0)
        for right_paddle_rectangle in right_paddle.rectangles:
            pygame.draw.rect(game_display, WHITE, right_paddle_rectangle, 0)
    pygame.draw.rect(game_display, WHITE, ball, 0)


def main():
    """Initialize the game and keep track of the gameplay through a loop"""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    game_font = pygame.freetype.Font("bit5x3.ttf", size=FONT_SIZE)
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("gnop")  # window title
    game_clock = pygame.time.Clock()
    left_paddle = Paddle(LEFT_PADDLE_X, LEFT_PADDLE_Y)
    right_paddle = Paddle(RIGHT_PADDLE_X, RIGHT_PADDLE_Y)
    ball = Ball()
    # Main loop
    playing = False
    quit_signal = False

    while not quit_signal:

        if not playing:
            # Print a quick how to play
            game_font.render_to(game_display, (0, 0), "WASD", WHITE)
            # To print "ARROWS" right-aligned, the width of a rectangle holding this text is used as a reference
            # Along the same line, the average scaled size (in pixels) of the used font is used to keep "Enter: Start"
            # within the game's display
            arrows_text_width = game_font.get_rect("ARROWS", size=FONT_SIZE).size[0]
            game_font.render_to(
                game_display, (DISPLAY_WIDTH - arrows_text_width, 0), "ARROWS", WHITE
            )
            game_font.render_to(
                game_display,
                (0, DISPLAY_HEIGHT - game_font.get_sized_height()),
                "Enter: Start",
                WHITE,
            )

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_signal = True
        # Get input
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]:  # New game
            playing = True
            left_paddle.score = 0
            right_paddle.score = 0
            rally = 0
            ball = Ball()
        if playing:
            game_font.render_to(game_display, (0, 0), str(left_paddle.score), WHITE)
            # To print the right player's score right-aligned, the same approach as for the "ARROWS" text is used
            right_score_text_width = game_font.get_rect(
                str(right_paddle.score), size=FONT_SIZE
            ).size[0]
            game_font.render_to(
                game_display,
                (DISPLAY_WIDTH - right_score_text_width, 0),
                str(right_paddle.score),
                WHITE,
            )
            handle_players_input(pressed_keys, left_paddle, right_paddle)
            side_wall_hit, rally = ball.handle_collisions(
                left_paddle, right_paddle, rally
            )
            if side_wall_hit:
                pygame.mixer.music.load("beep-03.wav")
                pygame.mixer.music.play()
                update_score(side_wall_hit, left_paddle, right_paddle)
                after_point_orientation = get_after_point_orientation(ball)
                ball = Ball(after_point_orientation)
                rally = 0
            if left_paddle.score == MAX_SCORE or right_paddle.score == MAX_SCORE:
                playing = False
        else:
            ball.bounce_from_walls()

        pygame.display.update()  # Renders the display

        ball.move()
        draw_background(game_display)
        draw_gameplay(game_display, left_paddle, right_paddle, ball, playing)
        game_clock.tick(60)  # FPS
    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
