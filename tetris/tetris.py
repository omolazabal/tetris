
import pygame
from pygame.locals import *
from .core import tetromino, grid


class Game():
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 480
        self.grid_height = 20
        self.grid_width = 10
        self.key_repeat_delay = 150
        self.key_repeat_interval = 30

    def set_grid_width(self, width):
        self.grid_width = width

    def set_grid_height(self, height):
        self.grid_height = height

    def set_grid_dim(self, dim):
        self.grid_width = dim[0]
        self.grid_height = dim[1]

    def set_screen_width(self, width):
        self.screen_width = width

    def set_screen_height(self, height):
        self.screen_height = height

    def set_screen_dim(self, dim):
        self.screen_width = dim[0]
        self.screen_height = dim[1]

    def set_key_repeat_delay(self, delay):
        self.key_repeat_delay = delay

    def set_key_repeat_interval(self, interval):
        self.key_repeat_interval = interval

    def print_grid(self):
        print('\n', self.tetromino.shape(),
              '\n', self.grid.grid[3:, 3:self.grid_width+3])

    def play(self):
        pygame.init()
        pygame.key.set_repeat(self.key_repeat_delay, self.key_repeat_interval)
        pygame.display.set_mode((self.screen_width, self.screen_height))

        self.grid = grid.Grid(self.grid_width, self.grid_height)
        self.tetromino = tetromino.Tetromino(self.grid_width)
        self._start_game()

    def quit(self):
        pygame.quit()
        exit(0)

    def _start_game(self):
        while True:
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT or keys_pressed[K_q]:
                    self.quit()
                elif keys_pressed[K_DOWN]:
                    self.tetromino.move_down()
                elif keys_pressed[K_LEFT]:
                    self.tetromino.move_left()
                elif keys_pressed[K_RIGHT]:
                    self.tetromino.move_right()
                elif keys_pressed[K_UP]:
                    self.tetromino.rotate()
                elif keys_pressed[K_n]:
                    self.tetromino.new_shape()

                if self.grid.update_grid(self.tetromino):
                    self.tetromino.new_shape()

                self.print_grid()
        pygame.quit()
