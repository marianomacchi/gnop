#!/bin/python3

# TODO:
# 1) ball class
# 2) gameplay
# 3) use pygame fonts and text to keep scorings

import pygame

class Colors:
    black = (0 , 0, 0) # RGB
    white = (255 , 255, 255)

class Display:
    width = 640
    height = 320
    center = width // 2
    # paddles' starting coordinates
    left_paddle_y = (int)(height * 0.45) # half of display, on the left
    left_paddle_x = (int)(width * 0.20)
    right_paddle_y = (int)(height * 0.45) # half of display, on the right
    right_paddle_x = (int)(width * 0.80)

class Paddle:
    height = 25
    width = 10
    def __init__(self, x, y):
        self.x = x # coordinates
        self.y = y
        # paddle's rectangle (used for movements and collisions)
        self.rect = pygame.Rect(self.x, self.y, Paddle.width, Paddle.height)

def init():
    pygame.init()
    game_display = pygame.display.set_mode((Display.width, Display.height))
    pygame.display.set_caption('gnop') # display title
    return game_display

def draw_background(game_display):
    game_display.fill(Colors.black)
    # draw central line (line segments are drawn from the top every 15 pixels)
    for y in range(Display.height+1):
        if y%15 == 0:
            pygame.draw.line(game_display, Colors.white, (Display.center, y),
                            (Display.center, y+5), 3) # thick=3

def draw_gameplay(game_display, LeftPaddle, RightPaddle):
    # draw paddles (0 fills the rectangles, 1 leaves them empty)
    pygame.draw.rect(game_display, Colors.white, LeftPaddle, 0)
    pygame.draw.rect(game_display, Colors.white, RightPaddle, 0)

def main():
    game_display = init()
    game_display_rect = game_display.get_rect() # used for collisions
    game_clock = pygame.time.Clock()
    # create paddles
    LeftPaddle = Paddle(Display.left_paddle_x, Display.left_paddle_y)
    RightPaddle = Paddle(Display.right_paddle_x, Display.right_paddle_y)
    # main loop
    quit_signal = False
    while not quit_signal:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_signal = True
        pressed_keys = pygame.key.get_pressed() # list of pressed keys
        # Left paddle movements
        if pressed_keys[pygame.K_w]:
            LeftPaddle.rect.move_ip(0, -5) # move up
        if pressed_keys[pygame.K_s]:
            LeftPaddle.rect.move_ip(0, 5) # move down
        # Right paddle movements
        if pressed_keys[pygame.K_UP]:
            RightPaddle.rect.move_ip(0, -5) # move up
        if pressed_keys[pygame.K_DOWN]:
            RightPaddle.rect.move_ip(0, 5) # move down
        # ensure paddles are inside the game display
        LeftPaddle.rect.clamp_ip(game_display_rect)
        RightPaddle.rect.clamp_ip(game_display_rect)
        # TODO: check ball
        draw_background(game_display)
        # draw the paddles and the ball
        draw_gameplay(game_display, LeftPaddle, RightPaddle)
        pygame.display.update() # renders the display
        game_clock.tick(60) # FPS
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
