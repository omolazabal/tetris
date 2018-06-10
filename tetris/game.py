
import pygame
from pygame.locals import *
from .core import tetromino, board
from .settings import Settings


class Game():
    """Class to run Tetris game."""

    def __init__(self):
        self.settings = Settings()
        self.board = None
        self.tetromino = None
        self.debug = False

    def _debug_print(self):
        print(self.tetromino)
        print(self.tetromino.position())
        print(self.tetromino.block_coordinates())
        print(self.board)
        print(self.board.get_height())

    def start(self):
        """Start the game."""
        # Init pygame
        pygame.init()
        pygame.key.set_repeat(self.settings.keyboard.key_repeat_delay,
                self.settings.keyboard.key_repeat_interval)
        pygame.display.set_mode((self.settings.display.width,
                                 self.settings.display.height))
        pygame.mouse.set_visible(0)

        # User events
        self.MOVE_DOWN = pygame.USEREVENT + 1

        # Time
        pygame.time.set_timer(self.MOVE_DOWN,
                self.settings.tetromino.speed)
        self.clock = pygame.time.Clock()

        # Init Tetris components
        self.board = board.Board(self.settings.board.width,
                self.settings.board.height)
        self.tetromino = tetromino.Tetromino(self.settings.board.width)

        self._play()

    def quit(self):
        pygame.quit()
        exit(0)

    def _play(self):
        """Begin game and check for keyboard inputs."""
        while True:
            self.clock.tick(self.settings.display.fps)
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT or keys_pressed[K_q]:
                    self.quit()

                elif event.type == self.MOVE_DOWN:
                    self.tetromino.soft_drop()

                elif keys_pressed[K_DOWN]:
                    self.tetromino.soft_drop()
                    pygame.time.set_timer(self.MOVE_DOWN,
                            self.settings.tetromino.speed)

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

            if self.debug:
                self._debug_print()

        pygame.quit()
