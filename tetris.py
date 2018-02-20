
import pygame
from pygame.locals import *
import tetromino
import grid

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_HEIGHT = 20
GRID_WIDTH = 10
KEY_REPEAT_DELAY = 150
KEY_REPEAT_INTERVAL = 30

# Init Pygame
pygame.init()
pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
game_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Init Tetris
tetris_board = grid.Grid(GRID_WIDTH, GRID_HEIGHT)
shape = tetromino.Tetromino(GRID_WIDTH)
shape.new_shape()
quit = False

def update():
    if tetris_board.update_grid(shape):
        if tetris_board.top_out_occured():
            tetris_board.new_grid()
        tetris_board.clear_line_check()
        shape.new_shape()

    print()
    print(shape.shape())
    print()
    print(tetris_board.grid[3:, 3:GRID_WIDTH+3])
    # print(tetris_board.grid)

while not quit:
    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT or keys_pressed[K_q]:
            quit = True
        elif keys_pressed[K_DOWN]:
            shape.move_down()
            update()
        elif keys_pressed[K_LEFT]:
            shape.move_left()
            update()
        elif keys_pressed[K_RIGHT]:
            shape.move_right()
            update()
        elif keys_pressed[K_UP]:
            shape.rotate()
            update()
        elif keys_pressed[K_n]:
            shape.new_shape()
            update()

pygame.quit()
exit(0)

