
import pygame
from pygame.locals import *
from .core import tetromino, board


class Game():
    """Class to run Tetris game."""

    def __init__(self):
        """Set default game settings."""
        self.screen_width = 468
        self.screen_height = 60
        self.board_height = 20
        self.board_width = 10
        self.key_repeat_delay = 150
        self.key_repeat_interval = 30
        self.speed = 1000

        self.board = None
        self.tetromino = None

    def debug_print(self):
        print(self.tetromino, '\n\n',
              self.board, '\n\n',
              self.board.get_height())

    def set_board_dim(self, dim):
        self.board_width = dim[0]
        self.board_height = dim[1]

    def set_screen_dim(self, dim):
        self.screen_width = dim[0]
        self.screen_height = dim[1]

    def set_key_repeat_delay(self, delay):
        self.key_repeat_delay = delay

    def set_key_repeat_interval(self, interval):
        self.key_repeat_interval = interval

    def set_speed(self, speed):
        self.speed = speed

    def play(self):
        """Start the game."""
        pygame.init()
        pygame.key.set_repeat(self.key_repeat_delay, self.key_repeat_interval)
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.mouse.set_visible(0)

        # Time settings
        self.MOVE_DOWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_DOWN, self.speed)
        self.clock = pygame.time.Clock()

        # Create Tetris objects
        self.board = board.Board(self.board_width, self.board_height)
        self.tetromino = tetromino.Tetromino(self.board_width)

        self._start_game()

    def quit(self):
        pygame.quit()
        exit(0)

    def _start_game(self):
        """Begin game and check for keyboard inputs."""
        fast = False
        while True:
            self.clock.tick(30)
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT or keys_pressed[K_q]:
                    self.quit()

                elif event.type == self.MOVE_DOWN:
                    self.tetromino.soft_drop()

                elif keys_pressed[K_DOWN]:
                    self.tetromino.soft_drop()
                    pygame.time.set_timer(self.MOVE_DOWN, self.speed)

                elif keys_pressed[K_LEFT]:
                    self.tetromino.move_left()

                elif keys_pressed[K_RIGHT]:
                    self.tetromino.move_right()

                elif keys_pressed[K_UP]:
                    self.tetromino.rotate()

                elif keys_pressed[K_n]:
                    self.tetromino.new_shape()

                if self.board.update_board(self.tetromino):
                    self.tetromino.new_shape()

            self.debug_print()

        pygame.quit()
