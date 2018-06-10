
import os
import time
import pygame
from pygame.locals import *
from .core import tetromino, board
from .settings import Settings


class Game:
    """Class to run Tetris game."""

    def __init__(self):
        self.settings = Settings()
        self.board = None
        self.tetromino = None
        self.debug = False
        self.pause = False
        self.start_time = time.time()

    def _debug_print(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print('\nPosition')
        print(self.tetromino.position())
        print('\nBlock coordinates')
        print(self.tetromino.block_coordinates())

        print('{:<17}{:<15}'.format('\nTetromino', 'Held'))
        for x, y in zip(self.tetromino.current_tetromino(),
                self.tetromino.held_tetromino()):
            print('{:<13}{:<15}'.format(str(x), str(y)))

        print('\nBoard')
        print(self.board)

        print('\nBoard heights')
        print(self.board.get_height())

        print('\nRun time')
        print('{:<8}{:<12}'.format(round((time.time() - self.start_time), 2),
              'seconds'))

        if self.pause:
            print('\nPaused')

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
        pygame.time.set_timer(self.MOVE_DOWN, self.settings.tetromino.speed)
        self.clock = pygame.time.Clock()

        # Init Tetris components
        self.board = board.Board()
        self.tetromino = tetromino.Tetromino()

        self._play()

    def _play(self):
        """Begin game and check for keyboard inputs."""
        while True:
            if self.board.top_out:
                self.board.reset()
                self.tetromino.reset()

            if self.board.update_board(self.tetromino):
                self.tetromino.new_shape()

            self.clock.tick(self.settings.display.fps)
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():

                if keys_pressed[K_ESCAPE]:
                    self._pause()

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
                    self.tetromino.rotate_right()

                elif keys_pressed[K_z]:
                    self.tetromino.rotate_left()

                elif keys_pressed[K_x]:
                    self.tetromino.hold()

                elif keys_pressed[K_SPACE]:
                    self.tetromino.hard_drop()
                    self.board.update_board(self.tetromino)
                    self.tetromino.soft_drop()

                # elif keys_pressed[K_n]:
                #     self.tetromino.new_shape()

            if self.debug:
                self._debug_print()

        pygame.quit()

    def _pause(self):
        self.pause = True
        while self.pause:
            self.clock.tick(self.settings.display.fps)
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT or keys_pressed[K_q]:
                    self._quit()

                if keys_pressed[K_ESCAPE]:
                    self.pause = False

            if self.debug:
                self._debug_print()

    def _quit(self):
        pygame.quit()
        exit(0)
