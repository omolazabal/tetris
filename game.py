
import os
import time
import pygame
import numpy as np
from pygame.locals import *
from core import tetromino, board
from settings import Settings


class Game:
    """Class to run Tetris game."""

    def __init__(self):
        self.settings = Settings()
        self.board = None
        self.tetromino = None
        self.debug = False
        self.pause = False
        self.display = None
        self.start_time = time.time()

        self.tile_size = 32
        self.top_boundary = 48
        self.bottom_boundary = 752
        self.left_boundary = 240
        self.right_boundary = 592

        self.background_img = pygame.image.load('assets/background.png')
        self.shadow_imgs = {
            'blue' : pygame.image.load('assets/blue_shadow.png'),
            'red' : pygame.image.load('assets/red_shadow.png'),
            'yellow' : pygame.image.load('assets/yellow_shadow.png'),
            'orange' : pygame.image.load('assets/orange_shadow.png'),
            'cyan' : pygame.image.load('assets/cyan_shadow.png'),
            'purple' : pygame.image.load('assets/purple_shadow.png'),
        }
        self.tetromino_imgs = {
            'blue' : pygame.image.load('assets/blue_tetromino.png'),
            'red' : pygame.image.load('assets/red_tetromino.png'),
            'yellow' : pygame.image.load('assets/yellow_tetromino.png'),
            'orange' : pygame.image.load('assets/orange_tetromino.png'),
            'cyan' : pygame.image.load('assets/cyan_tetromino.png'),
            'purple' : pygame.image.load('assets/purple_tetromino.png'),
        }

    def _debug_print(self):
        """Print Tetris pieces and relevant information to console."""
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
        pygame.display.set_caption('Tetris')
        self.display = pygame.display.set_mode((self.settings.display.width,
                                 self.settings.display.height))
        pygame.key.set_repeat(self.settings.keyboard.key_repeat_delay,
                self.settings.keyboard.key_repeat_interval)
        pygame.mouse.set_visible(0)

        # User events
        self.MOVE_DOWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_DOWN, self.settings.tetromino.speed)

        # Time
        self.clock = pygame.time.Clock()

        # Init Tetris components
        self.board = board.Board()
        self.tetromino = tetromino.Tetromino()

        self._play()

    def draw_shadow(self):
        coords = self.board.shadow.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.shadow_imgs[self.tetromino.color],
                    (self.left_boundary + self.tile_size + (x - 3)*32,
                     self.top_boundary + self.tile_size + (y - 3)*32))

    def draw_tetromino(self):
        coords = self.tetromino.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.color],
                    (self.left_boundary + self.tile_size + (x - 3)*32,
                     self.top_boundary + self.tile_size + (y - 3)*32))

    def _play(self):
        """Begin game and check for keyboard inputs."""
        self.display.fill((31, 31, 31))
        self.display.blit(self.background_img, (self.left_boundary + self.tile_size, self.top_boundary + self.tile_size))
        self.background = self.display.copy()

        while True:
            if self.board.top_out:
                self.board.reset()
                self.tetromino.reset()

            if self.board.update_board(self.tetromino):
                self.background = self.display.copy()
                self.tetromino.new_shape()

            self.clock.tick(self.settings.display.fps)
            self.display.blit(self.background, (0, 0))
            self.draw_shadow()
            self.draw_tetromino()
            pygame.display.update()

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

                    self.display.blit(self.background, (0, 0))
                    self.draw_tetromino()
                    pygame.display.update()
                    self.background = self.display.copy()

                    self.tetromino.soft_drop()

                elif keys_pressed[K_n]:
                    self.tetromino.new_shape()

            if self.board.filled_rows.size != 0:
                # do fancy choppy croppy stuffs
                print(self.board.filled_rows)
                self.board.filled_rows = np.array([])

            if self.debug:
                self._debug_print()

        pygame.quit()

    def _pause(self):
        """Pause gameplay."""
        self.pause = True
        while self.pause:
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT or keys_pressed[K_q]:
                    self._quit()

                if keys_pressed[K_ESCAPE]:
                    self.pause = False

            if self.debug:
                self._debug_print()

            pygame.display.update()
            self.clock.tick(self.settings.display.fps)

    def _quit(self):
        """Quit the program."""
        pygame.quit()
        quit()
