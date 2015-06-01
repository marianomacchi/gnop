#!/bin/python3

# TODO:
# 1) make a paddle class?
# 2) make a ball class?
# 3) gameplay
# 4) use pygame fonts and text to keep scorings
# 3) group functions based on functionality (e.g.: draw_background(), etc)

import pygame

# Init: display and clock
pygame.init()
display_width = 640
display_height = 320
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('gnop') # display title
game_clock = pygame.time.Clock()

# RGB colors!
white = (255 , 255, 255)
black = (0 , 0, 0)
# Paddles' length and width
paddle_height = 25
paddle_width = 10

# Paddles' starting coordinates
lpaddle_y = (int)(display_height * 0.45) # half of display, on the left
lpaddle_x = (int)(display_width * 0.20)
rpaddle_y = (int)(display_height * 0.45) # half of display, on the right
rpaddle_x = (int)(display_width * 0.80)

# display's central point
central_point = display_width // 2

# game display rectangle (for collisions)
game_display_rect = game_display.get_rect()

# Left and Right paddles
lpaddle = pygame.Rect(lpaddle_x, lpaddle_y, paddle_width, paddle_height)
rpaddle = pygame.Rect(rpaddle_x, rpaddle_y, paddle_width, paddle_height)

# main loop
quit_signal = False
while not quit_signal:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            quit_signal = True
    pressed_keys = pygame.key.get_pressed() # list? dict? of pressed keys
    # Left paddle movements
    if pressed_keys[pygame.K_w]:
        lpaddle.move_ip(0, -5) # move up
    if pressed_keys[pygame.K_s]:
        lpaddle.move_ip(0, 5) # move down
    # Right paddle movements
    if pressed_keys[pygame.K_UP]:
        rpaddle.move_ip(0, -5) # move up
    if pressed_keys[pygame.K_DOWN]:
        rpaddle.move_ip(0, 5) # move down

    # draw background
    game_display.fill(black)
    # draw central line
    for y in range(display_height+1):
        # draw small line segments every 15 pixels, starting from the top
        if y%15 == 0:
            pygame.draw.line(game_display, white, (central_point, y),
                            (central_point , y+5), 3)

    # ensure paddles are inside the game display
    lpaddle.clamp_ip(game_display_rect)
    rpaddle.clamp_ip(game_display_rect)
    # draw paddles
    pygame.draw.rect(game_display, white, lpaddle, 0) # 0 fills the rect
    pygame.draw.rect(game_display, white, rpaddle, 0) # 0 fills the rect
    pygame.display.update() # updates only parts of the screen
    game_clock.tick(60) # FPS

pygame.quit()
quit()
