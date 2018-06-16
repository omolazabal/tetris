
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
    FONT_SIZE = 32

    BACKGROUND_LOC = (LEFT, TOP)
    BACKGROUND_BORDER_LOC = (LEFT - TILE_SIZE//8, TOP - TILE_SIZE//8)

    SIDE_BACKGROUND_LOC = (LEFT - TILE_SIZE*6 - TILE_SIZE//4, TOP + TILE_SIZE*4)
    SIDE_BACKGROUND_BORDER_LOC = (SIDE_BACKGROUND_LOC[0] - TILE_SIZE//8, SIDE_BACKGROUND_LOC[1] - TILE_SIZE//8)
    SIDE_TET_LOC = {
        'I' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE/2, SIDE_BACKGROUND_LOC[1] + TILE_SIZE/2),
        'O' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE/2, SIDE_BACKGROUND_LOC[1] + TILE_SIZE),
        'L' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE, SIDE_BACKGROUND_LOC[1] + TILE_SIZE),
        'J' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE, SIDE_BACKGROUND_LOC[1] + TILE_SIZE),
        'T' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE, SIDE_BACKGROUND_LOC[1] + TILE_SIZE),
        'Z' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE, SIDE_BACKGROUND_LOC[1] + TILE_SIZE),
        'S' : (SIDE_BACKGROUND_LOC[0] + TILE_SIZE, SIDE_BACKGROUND_LOC[1] + TILE_SIZE),
    }
    SIDE_FONT_LOC = (SIDE_BACKGROUND_LOC[0] + TILE_SIZE*1.1, SIDE_BACKGROUND_LOC[1] - TILE_SIZE*1.5)

    def __init__(self):
        pg.init()

        self.board = None
        self.tetromino = None
        self.debug = False
        self.paused = False
        self.display = None

        self.background_img = 'tetris/assets/background.png'
        self.background_border_img = 'tetris/assets/background_border.png'
        self.side_background_img = 'tetris/assets/side_background.png'
        self.side_background_border_img = 'tetris/assets/side_background_border.png'
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
        self.background_border = pg.image.load(self.background_border_img)
        self.side_background = pg.image.load(self.side_background_img)
        self.side_background_border = pg.image.load(self.side_background_border_img)
        self.cover = pg.Surface((384, 80))
        self.cover.fill((27, 27, 27))

        self.font_name = pg.font.match_font('arial', 1)
        self.held_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('HELD', True, (255, 255, 255))
        self.next_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('NEXT', True, (255, 255, 255))

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
        pg.display.set_caption('Tetris')
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
                        (self.SIDE_TET_LOC[self.board.held_tetromino.shape][0] + (x - self.board.held_tetromino.col)*32,
                        self.SIDE_TET_LOC[self.board.held_tetromino.shape][1] + (y - 3)*32 + self.TILE_SIZE*8))

    def blit_next_tetromino(self):
        coords = self.tetromino.next_block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.next_color],
                    (self.SIDE_TET_LOC[self.tetromino.next_shape][0] + x*32,
                    self.SIDE_TET_LOC[self.tetromino.next_shape][1] + y*32))

    def blit_tetromino(self):
        coords = self.tetromino.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*32,
                     self.BACKGROUND_LOC[1] + (y - 3)*32))

    def get_new_background(self):
        self.background = self.display.copy().subsurface(
                (self.BACKGROUND_LOC), (320, 640))

    def render_frame(self):
        self.display.fill((27, 27, 27))
        self.display.blit(self.background, self.BACKGROUND_LOC)
        self.blit_shadow()
        self.blit_tetromino()
        self.display.blit(self.side_background, (self.SIDE_BACKGROUND_LOC[0], self.SIDE_BACKGROUND_LOC[1] + self.TILE_SIZE*8))
        self.display.blit(self.side_background, self.SIDE_BACKGROUND_LOC)
        self.blit_held_tetromino()
        self.blit_next_tetromino()
        self.display.blit(self.cover, (self.LEFT, 0))
        self.display.blit(self.background_border, self.BACKGROUND_BORDER_LOC)
        self.display.blit(self.side_background_border, (self.SIDE_BACKGROUND_BORDER_LOC[0], self.SIDE_BACKGROUND_BORDER_LOC[1] + self.TILE_SIZE*8))
        self.display.blit(self.side_background_border, self.SIDE_BACKGROUND_BORDER_LOC)
        self.display.blit(self.held_font, (self.SIDE_FONT_LOC[0], self.SIDE_FONT_LOC[1] + self.TILE_SIZE*8))
        self.display.blit(self.next_font, self.SIDE_FONT_LOC)


    def play(self):
        """Begin game and check for keyboard inputs."""
        self.board.update_board(self.tetromino)

        while True:
            if self.board.top_out:
                self.board.reset()
                self.tetromino.reset()
                self.board.update_board(self.tetromino)
                self.background = pg.image.load(self.background_img)

            if self.board.filled_rows.size != 0:
                chop = pg.transform.chop(self.background,
                        (0, self.TILE_SIZE*np.min(self.board.filled_rows - 3),
                         0, self.TILE_SIZE*self.board.filled_rows.size))
                self.display.blit(chop,
                        (self.BACKGROUND_LOC[0], self.BACKGROUND_LOC[1] +
                            self.TILE_SIZE*self.board.filled_rows.size))
                self.get_new_background()
                self.board.filled_rows = np.array([])

            self.clock.tick(DisplaySettings.fps)
            self.render_frame()
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
