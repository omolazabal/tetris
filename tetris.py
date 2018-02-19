
import pygame as pg
import sys, termios, tty, os, time
import tetromino
import grid

GRID_HEIGHT = 20
GRID_WIDTH = 10

tetris_board = grid.Grid(GRID_WIDTH, GRID_HEIGHT)
shape = tetromino.Tetromino(GRID_WIDTH)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


shape.new_shape()
print(tetris_board.grid[3:, 3:GRID_WIDTH+3])
# print(tetris_board.grid)

while True:
    char = getch()

    if (char == "q"):
        exit(0)

    if (char == "r"):
        shape.rotate()

    if (char == "h"):
        shape.move_left()

    if (char == "j"):
        shape.move_down()

    if (char == "l"):
        shape.move_right()

    if (char == "n"):
        shape.new_shape()

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



