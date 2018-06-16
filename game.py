
import os
import pygame as pg
import numpy as np
from pygame.locals import *
from tetris.utils import Timer
from tetris.core import Tetromino, Board
from tetris.settings import *


class Game:
    """Class to run Tetris game."""

    TILE_SIZE = 32
    TOP = 80
    BOTTOM = 80
    LEFT = 240
    RIGHT = 560
    BACKGROUND_LOC = (LEFT, TOP)
    HELD_BACKGROUND_LOC = (LEFT - TILE_SIZE*6 - 8, TOP + TILE_SIZE*5)
    HELD_TET_LOC = {
        'I' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE/2, HELD_BACKGROUND_LOC[1] + TILE_SIZE/2),
        'O' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE/2, HELD_BACKGROUND_LOC[1] + TILE_SIZE),
        'L' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE, HELD_BACKGROUND_LOC[1] + TILE_SIZE),
        'J' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE, HELD_BACKGROUND_LOC[1] + TILE_SIZE),
        'T' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE, HELD_BACKGROUND_LOC[1] + TILE_SIZE),
        'Z' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE, HELD_BACKGROUND_LOC[1] + TILE_SIZE),
        'S' : (HELD_BACKGROUND_LOC[0] + TILE_SIZE, HELD_BACKGROUND_LOC[1] + TILE_SIZE),
    }

    def __init__(self):
        self.board = None
        self.tetromino = None
        self.debug = False
        self.paused = False
        self.display = None

        self.tile_size = 32
        self.top_boundary = 48
        self.bottom_boundary = 752
        self.left_boundary = 240
        self.right_boundary = 592
        self.background_loc = (240, 80)

        self.background_img = 'tetris/assets/background.png'
        self.held_background_img = 'tetris/assets/held_background.png'
        self.shadow_imgs = {
            'blue' : pg.image.load('tetris/assets/blue_shadow.png'),
            'red' : pg.image.load('tetris/assets/red_shadow.png'),
            'yellow' : pg.image.load('tetris/assets/yellow_shadow.png'),
            'orange' : pg.image.load('tetris/assets/orange_shadow.png'),
            'cyan' : pg.image.load('tetris/assets/cyan_shadow.png'),
            'purple' : pg.image.load('tetris/assets/purple_shadow.png'),
        }
        self.tetromino_imgs = {
            'blue' : pg.image.load('tetris/assets/blue_tile.png'),
            'red' : pg.image.load('tetris/assets/red_tile.png'),
            'yellow' : pg.image.load('tetris/assets/yellow_tile.png'),
            'orange' : pg.image.load('tetris/assets/orange_tile.png'),
            'cyan' : pg.image.load('tetris/assets/cyan_tile.png'),
            'purple' : pg.image.load('tetris/assets/purple_tile.png'),
        }

        self.background = pg.image.load(self.background_img)
        self.held_background = pg.image.load(self.held_background_img)

    def debug_print(self):
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
        # Init pg
        pg.init()
        pg.display.set_caption('Tetris')
        pg.mouse.set_visible(0)
        self.display = pg.display.set_mode((DisplaySettings.width, DisplaySettings.height))

        # User events
        self.MOVE_DOWN = pg.USEREVENT + 1
        pg.time.set_timer(self.MOVE_DOWN, TimerSettings.drop_interval)
        pg.key.set_repeat(KeyboardSettings.delay, KeyboardSettings.interval)

        # Time
        self.clock = pg.time.Clock()

        # Init Tetris components
        self.board = Board()
        self.tetromino = Tetromino()

        self.play()

    def blit_shadow(self):
        coords = self.board.shadow.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.shadow_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*32,
                     self.BACKGROUND_LOC[1] + (y - 3)*32))

    def blit_held_tetromino(self):
        if self.board.held_tetromino is not None:
            pos= self.board.held_tetromino.position()
            coords = self.board.held_tetromino.block_coordinates()
            for x, y in zip(coords[1], coords[0]):
                self.display.blit(self.tetromino_imgs[self.board.held_tetromino.color],
                        (self.HELD_TET_LOC[self.board.held_tetromino.shape][0] + (x - self.board.held_tetromino.col)*32,
                        self.HELD_TET_LOC[self.board.held_tetromino.shape][1] + (y - 3)*32))

    def blit_tetromino(self):
        coords = self.tetromino.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*32,
                     self.BACKGROUND_LOC[1] + (y - 3)*32))

    def get_new_background(self):
        self.background = self.display.copy().subsurface(
                (self.BACKGROUND_LOC), (320, 640))

    def play(self):
        """Begin game and check for keyboard inputs."""
        cover = pg.Surface((384, 80))
        cover.fill((32, 32, 32))
        self.board.update_board(self.tetromino)

        while True:
            if self.board.top_out:
                self.board.reset()
                self.tetromino.reset()
                self.board.update_board(self.tetromino)
                self.background = pg.image.load(self.background_img)

            if self.board.filled_rows.size != 0:
                chop = pg.transform.chop(self.background,
                        (0, self.tile_size*np.min(self.board.filled_rows - 3),
                         0, self.tile_size*self.board.filled_rows.size))
                self.display.blit(chop,
                        (self.BACKGROUND_LOC[0], self.BACKGROUND_LOC[1] +
                            self.tile_size*self.board.filled_rows.size))
                self.get_new_background()
                self.board.filled_rows = np.array([])

            self.clock.tick(DisplaySettings.fps)

            self.display.fill((32, 32, 32))
            self.display.blit(self.background, self.BACKGROUND_LOC)
            self.blit_shadow()
            self.blit_tetromino()
            self.display.blit(self.held_background, self.HELD_BACKGROUND_LOC)
            self.blit_held_tetromino()
            self.display.blit(cover, (self.LEFT, 0))
            pg.display.update()

            for event in pg.event.get():
                if event.type == self.MOVE_DOWN:
                    if self.board.soft_drop(self.tetromino):
                        self.get_new_background()

                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_DOWN:
                        if self.board.soft_drop(self.tetromino):
                            self.get_new_background()
                        pg.time.set_timer(self.MOVE_DOWN, TimerSettings.drop_interval)

                    if event.key == pg.K_LEFT:
                        self.board.move_left(self.tetromino)

                    elif event.key == pg.K_RIGHT:
                        self.board.move_right(self.tetromino)

                    if event.key == pg.K_ESCAPE:
                        self.pause()

                    elif event.key == pg.K_x:
                        self.board.hold(self.tetromino)

                    elif event.key == pg.K_z:
                        self.board.rotate_left(self.tetromino)
                        pg.key.set_repeat(KeyboardSettings.delay, KeyboardSettings.interval)

                    elif event.key == pg.K_UP:
                        self.board.rotate_right(self.tetromino)

                    elif event.key == pg.K_SPACE:
                        self.board.hard_drop(self.tetromino)
                        self.display.blit(self.background, self.BACKGROUND_LOC)
                        self.blit_tetromino()
                        self.board.soft_drop(self.tetromino)
                        self.get_new_background()

            if self.debug:
                self.debug_print()

        pg.quit()

    def pause(self):
        """Pause gameplay."""
        self.paused = True
        while self.paused:
            pg.display.update()
            self.clock.tick(DisplaySettings.fps)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.quit()

                    if event.key == pg.K_ESCAPE:
                        self.paused = False

            if self.debug:
                self.debug_print()


    def quit(self):
        """Quit the program."""
        pg.quit()
        quit()
