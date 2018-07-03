
import os
import pickle
import pygame as pg
import numpy as np
import datetime
from pygame.locals import *
from tetris.utils import Timer
from tetris.core import Tetromino, Board, Score
from tetris.settings import *


class Game:
    """Class to run Tetris game."""

    TILE_SIZE = TetrominoSettings.tile_size
    TOP = DisplaySettings.height//10
    BOTTOM = DisplaySettings.height//10
    LEFT = (DisplaySettings.width-TILE_SIZE*10)//2
    RIGHT = DisplaySettings.width-LEFT

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

    HELD_FONT_LOC = (SIDE_FONT_LOC[0], SIDE_FONT_LOC[1] + TILE_SIZE*8)
    SCORE_FONT_LOC = (SIDE_FONT_LOC[0] + TILE_SIZE*16, SIDE_FONT_LOC[1])
    SCORE_NUM_LOC = (SIDE_FONT_LOC[0] + TILE_SIZE*16, SIDE_FONT_LOC[1] + TILE_SIZE*2)
    HIGH_SCORE_FONT_LOC = (SCORE_FONT_LOC[0], SCORE_FONT_LOC[1] + TILE_SIZE*5)
    HIGH_SCORE_NUM_LOC = (SCORE_NUM_LOC[0], HIGH_SCORE_FONT_LOC[1] + TILE_SIZE*2)
    LEVEL_FONT_LOC = (SIDE_FONT_LOC[0] + TILE_SIZE*16, HIGH_SCORE_FONT_LOC[1] + TILE_SIZE*5) 
    LEVEL_NUM_LOC = (SIDE_FONT_LOC[0] + TILE_SIZE*16, LEVEL_FONT_LOC[1] + TILE_SIZE*2) 
    GAME_OVER_FONT_LOC = (DisplaySettings.width//4, DisplaySettings.height//2 - TILE_SIZE)

    FONT_SIZE = TILE_SIZE
    GAME_OVER_FONT_SIZE = TILE_SIZE*2
    BACKGROUND_COLOR = (27, 27, 27)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 0, 0)

    def __init__(self):
        pg.init()

        self.board = Board()
        self.tetromino = Tetromino()
        self.score = Score()
        self.debug = False
        self.paused = False
        self.display = None
        self.speed = TimerSettings.drop_interval
        self.background_img = 'tetris/assets/' + str(self.TILE_SIZE) + '/background.png'
        self.background_border_img = 'tetris/assets/' + str(self.TILE_SIZE) + '/background_border.png'
        self.side_background_img = 'tetris/assets/' + str(self.TILE_SIZE) + '/side_background.png'
        self.side_background_border_img = 'tetris/assets/' + str(self.TILE_SIZE) + '/side_background_border.png'

        self.scores = {str(datetime.datetime.now()):0}
        if os.path.getsize('scores') > 0:  
            with open ('scores', 'rb') as fp:
                self.scores = pickle.load(fp)

        self.shadow_imgs = {
            'blue' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/blue_shadow.png'),
            'red' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/red_shadow.png'),
            'yellow' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/yellow_shadow.png'),
            'orange' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/orange_shadow.png'),
            'cyan' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/cyan_shadow.png'),
            'purple' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/purple_shadow.png'),
        }
        self.tetromino_imgs = {
            'blue' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/blue_tile.png'),
            'red' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/red_tile.png'),
            'yellow' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/yellow_tile.png'),
            'orange' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/orange_tile.png'),
            'cyan' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/cyan_tile.png'),
            'purple' : pg.image.load('tetris/assets/' + str(self.TILE_SIZE) + '/purple_tile.png'),
        }

        self.background = pg.image.load(self.background_img)
        self.background_border = pg.image.load(self.background_border_img)
        self.side_background = pg.image.load(self.side_background_img)
        self.side_background_border = pg.image.load(self.side_background_border_img)
        self.cover = pg.Surface((self.LEFT, self.TOP))
        self.cover.fill(self.BACKGROUND_COLOR)

        self.font_name = pg.font.match_font('arial', 1)
        self.held_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('HOLD', True, self.WHITE)
        self.next_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('NEXT', True, self.WHITE)
        self.level_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('LEVEL', True, self.WHITE)
        self.score_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('SCORE', True, self.WHITE)
        self.high_score_font = pg.font.Font(self.font_name, self.FONT_SIZE).render('HIGH SCORE', True, self.WHITE)
        self.game_over_font = pg.font.Font(self.font_name, self.GAME_OVER_FONT_SIZE).render('GAME OVER', True, self.RED)

    def debug_print(self):
        """Print Tetris pieces and relevant information to console."""
        os.system('cls' if os.name == 'nt' else 'clear')

        print('\nPosition')
        print(self.tetromino.position())
        print('\nBlock coordinates')
        print(self.tetromino.block_coordinates())
        print('\nBoard')
        print(self.board)
        print('\nBoard heights')
        print(self.board.get_height())

        if self.pause:
            print('\nPaused')

    def start(self):
        """Start the game."""
        pg.display.set_caption('Tetris')
        self.display = pg.display.set_mode((DisplaySettings.width, DisplaySettings.height))
        self.MOVE_DOWN = pg.USEREVENT + 1
        pg.time.set_timer(self.MOVE_DOWN, self.speed)
        pg.key.set_repeat(KeyboardSettings.delay, KeyboardSettings.interval)
        self.clock = pg.time.Clock()
        self.play()

    def blit_shadow(self):
        coords = self.board.shadow.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.shadow_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*self.TILE_SIZE,
                     self.BACKGROUND_LOC[1] + (y - 3)*self.TILE_SIZE))

    def blit_held_tetromino(self):
        if self.board.held_tetromino is not None:
            pos= self.board.held_tetromino.position()
            coords = self.board.held_tetromino.block_coordinates()
            for x, y in zip(coords[1], coords[0]):
                self.display.blit(self.tetromino_imgs[self.board.held_tetromino.color],
                        (self.SIDE_TET_LOC[self.board.held_tetromino.shape][0] + (x - self.board.held_tetromino.col)*self.TILE_SIZE,
                        self.SIDE_TET_LOC[self.board.held_tetromino.shape][1] + (y - 3)*self.TILE_SIZE + self.TILE_SIZE*8))

    def blit_next_tetromino(self):
        coords = self.tetromino.next_block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.next_color],
                    (self.SIDE_TET_LOC[self.tetromino.next_shape][0] + x*self.TILE_SIZE,
                    self.SIDE_TET_LOC[self.tetromino.next_shape][1] + y*self.TILE_SIZE))

    def blit_tetromino(self):
        coords = self.tetromino.block_coordinates()
        for x, y in zip(coords[1], coords[0]):
            self.display.blit(self.tetromino_imgs[self.tetromino.color],
                    (self.BACKGROUND_LOC[0] + (x - 3)*self.TILE_SIZE,
                     self.BACKGROUND_LOC[1] + (y - 3)*self.TILE_SIZE))

    def get_new_background(self):
        self.background = self.display.copy().subsurface((self.BACKGROUND_LOC), (self.TILE_SIZE*10, self.TILE_SIZE*20))

    def blit_text(self):
        score = pg.font.Font(self.font_name, self.FONT_SIZE).render(str(self.score.score), True, self.WHITE)
        level = pg.font.Font(self.font_name, self.FONT_SIZE).render(str(self.score.level), True, self.WHITE)
        high_score = pg.font.Font(self.font_name, self.FONT_SIZE).render(str(max(self.scores.values())), True, self.WHITE)
        self.display.blit(self.held_font, self.HELD_FONT_LOC)
        self.display.blit(self.next_font, self.SIDE_FONT_LOC)
        self.display.blit(self.level_font, self.LEVEL_FONT_LOC)
        self.display.blit(self.score_font, self.SCORE_FONT_LOC)
        self.display.blit(self.high_score_font, self.HIGH_SCORE_FONT_LOC)
        self.display.blit(score, self.SCORE_NUM_LOC)
        self.display.blit(high_score, self.HIGH_SCORE_NUM_LOC)
        self.display.blit(level, self.LEVEL_NUM_LOC)

    def render_frame(self):
        self.display.fill(self.BACKGROUND_COLOR)
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
        self.blit_text()

    def clear_line(self):
        chop = pg.transform.chop(self.background,
                (0, self.TILE_SIZE*np.min(self.board.filled_rows - 3),
                    0, self.TILE_SIZE*self.board.filled_rows.size))
        self.display.blit(chop,
                (self.BACKGROUND_LOC[0], self.BACKGROUND_LOC[1] +
                    self.TILE_SIZE*self.board.filled_rows.size))
        self.get_new_background()
        self.board.filled_rows = np.array([])

    def reset(self):
        self.score.reset()
        self.board.reset()
        self.tetromino.reset()
        self.board.update_board(self.tetromino)
        self.background = pg.image.load(self.background_img)


    def play(self):
        """Begin game and check for keyboard inputs."""
        self.board.update_board(self.tetromino)

        while True:
            if self.board.top_out:
                self.game_over()

            if self.board.filled_rows.size != 0:
                if self.score.add_score(self.board.filled_rows.size):
                    self.speed -= 75
                    pg.time.set_timer(self.MOVE_DOWN, self.speed)
                self.clear_line()

            self.clock.tick(DisplaySettings.fps)
            self.render_frame()
            pg.display.update()

            for event in pg.event.get():
                if event.type == self.MOVE_DOWN and not self.board.top_out:
                    if self.board.soft_drop(self.tetromino):
                        self.get_new_background()

                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_DOWN:
                        if self.board.soft_drop(self.tetromino):
                            self.get_new_background()
                        pg.time.set_timer(self.MOVE_DOWN, self.speed)

                    elif event.key == pg.K_LEFT:
                        self.board.move_left(self.tetromino)

                    elif event.key == pg.K_RIGHT:
                        self.board.move_right(self.tetromino)

                    elif event.key == pg.K_ESCAPE:
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
                    if event.key == pg.K_ESCAPE:
                        self.paused = False

            if self.debug:
                self.debug_print()

    def game_over(self):
        darken = pg.Surface((DisplaySettings.width, DisplaySettings.height))
        darken.set_alpha(175)
        darken.fill(self.BLACK)
        self.display.blit(darken, (0,0))
        self.display.blit(self.game_over_font, self.GAME_OVER_FONT_LOC)
        self.scores[str(datetime.datetime.now())] = self.score.score
        with open('scores', 'wb') as fp:
            pickle.dump(self.scores, fp)

        while True:
            pg.display.update()
            self.clock.tick(DisplaySettings.fps)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            if self.debug:
                self.debug_print()

    def quit(self):
        """Quit the program."""
        pg.quit()
        quit()
