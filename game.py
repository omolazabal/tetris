
import os
import pygame
import numpy as np
from pygame.locals import *
from tetris.utils import Timer
from tetris.core import Tetromino, Board
from tetris.settings import PrelaunchSettings


class Game:
    """Class to run Tetris game."""

    TILE_SIZE = 32
    TOP = 48
    BOTTOM = 752
    LEFT = 240
    RIGHT = 592
    BACKGROUND_LOC = (LEFT + TILE_SIZE, TOP + TILE_SIZE)

    def __init__(self):
        self.pre_settings = PrelaunchSettings()
        self.board = None
        self.tetromino = None
        self.debug = False
        self.pause = False
        self.display = None

        self.tile_size = 32
        self.top_boundary = 48
        self.bottom_boundary = 752
        self.left_boundary = 240
        self.right_boundary = 592
        self.background_loc = (self.left_boundary + self.tile_size,
                               self.top_boundary + self.tile_size)

        self.background_img = 'tetris/assets/background.png'
        self.background = pygame.image.load(self.background_img)
        self.shadow_imgs = {
            'blue' : pygame.image.load('tetris/assets/blue_shadow.png'),
            'red' : pygame.image.load('tetris/assets/red_shadow.png'),
            'yellow' : pygame.image.load('tetris/assets/yellow_shadow.png'),
            'orange' : pygame.image.load('tetris/assets/orange_shadow.png'),
            'cyan' : pygame.image.load('tetris/assets/cyan_shadow.png'),
            'purple' : pygame.image.load('tetris/assets/purple_shadow.png'),
        }
        self.tetromino_imgs = {
            'blue' : pygame.image.load('tetris/assets/blue_tile.png'),
            'red' : pygame.image.load('tetris/assets/red_tile.png'),
            'yellow' : pygame.image.load('tetris/assets/yellow_tile.png'),
            'orange' : pygame.image.load('tetris/assets/orange_tile.png'),
            'cyan' : pygame.image.load('tetris/assets/cyan_tile.png'),
            'purple' : pygame.image.load('tetris/assets/purple_tile.png'),
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

        if self.pause:
            print('\nPaused')

    def start(self):
        """Start the game."""
        # Init pygame
        pygame.init()
        pygame.display.set_caption('Tetris')
        pygame.mouse.set_visible(0)
        self.display = pygame.display.set_mode((self.pre_settings.display.width, self.pre_settings.display.height))

        # User events
        self.MOVE_DOWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_DOWN, self.pre_settings.tetromino.speed)
        pygame.key.set_repeat(self.pre_settings.keyboard.delay, self.pre_settings.keyboard.interval)

        # Time
        self.clock = pygame.time.Clock()

        # Init Tetris components
        self.board = Board()
        self.tetromino = Tetromino()

        self._play()

    def blit_shadow(self):
        coords = self.board.shadow.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.shadow_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*32,
                     self.BACKGROUND_LOC[1] + (y - 3)*32))

    def blit_tetromino(self):
        coords = self.tetromino.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*32,
                     self.BACKGROUND_LOC[1] + (y - 3)*32))

    def get_new_background(self):
        self.background = self.display.copy().subsurface(
                (self.BACKGROUND_LOC), (320, 640))

    def _play(self):
        """Begin game and check for keyboard inputs."""
        cover = pygame.Surface((384, 48))
        cover.fill((32, 32, 32))
        skip_shadow = False

        while True:
            if self.board.top_out:
                self.board.reset()
                self.tetromino.reset()
                self.background = pygame.image.load(self.background_img)

            if self.board.update_board(self.tetromino):
                self.get_new_background()
                self.tetromino.new_shape()
                skip_shadow = True

            if self.board.filled_rows.size != 0:
                self.display.blit(pygame.transform.chop(self.background,
                        (0, self.tile_size*np.min(self.board.filled_rows - 3),
                         0, self.tile_size*self.board.filled_rows.size)),
                        (self.BACKGROUND_LOC[0],
                            self.BACKGROUND_LOC[1] +
                            self.tile_size*self.board.filled_rows.size))
                self.get_new_background()
                self.board.filled_rows = np.array([])

            self.clock.tick(self.pre_settings.display.fps)
            self.display.fill((32, 32, 32))
            self.display.blit(self.background, self.BACKGROUND_LOC)
            if not skip_shadow:
                self.blit_shadow()
            skip_shadow = False
            self.blit_tetromino()
            self.display.blit(cover, (self.LEFT, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == self.MOVE_DOWN:
                    self.tetromino.soft_drop()

                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_DOWN:
                        self.tetromino.soft_drop()
                        pygame.time.set_timer(self.MOVE_DOWN,
                                self.pre_settings.tetromino.speed)

                    elif event.key == pygame.K_LEFT:
                        self.tetromino.move_left()

                    elif event.key == pygame.K_RIGHT:
                        self.tetromino.move_right()

                    if event.key == pygame.K_ESCAPE:
                        self._pause()

                    elif event.key == pygame.K_x:
                        self.tetromino.hold()

                    elif event.key == pygame.K_n:
                        self.tetromino.new_shape()

                    elif event.key == pygame.K_z:
                        self.tetromino.rotate_left()

                    elif event.key == pygame.K_UP:
                        self.tetromino.rotate_right()

                    elif event.key == pygame.K_SPACE:
                        self.board.hard_drop(self.tetromino)
                        self.board.update_board(self.tetromino)
                        self.display.blit(self.background, self.BACKGROUND_LOC)
                        self.blit_tetromino()
                        self.tetromino.soft_drop()

            if self.debug:
                self._debug_print()

        pygame.quit()

    def _pause(self):
        """Pause gameplay."""
        self.pause = True
        while self.pause:
            pygame.display.update()
            self.clock.tick(self.pre_settings.display.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._quit()

                    # if event.key == pygame.K_ESCAPE:
                    #     self.pause = False

            if self.debug:
                self._debug_print()


    def _quit(self):
        """Quit the program."""
        pygame.quit()
        quit()
