
import random
import numpy as np
import copy
from tetris.utils import SHAPES


class Board:
    """Class for the board in Tetris."""

    def __init__(self):
        """Set the settings for the Tetris board."""
        self.width = 10 + 6   # Accommodate for sides.
        self.height = 20 + 4  # Accommodate for base and spawn.
        self.left_boundary = 3
        self.right_boundary = self.width - 4

        self.fill_height = np.zeros((1, self.width), dtype=int)
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.board[self.height-1, :] = np.ones(self.width)*9
        self.filled_rows = np.array([])

        self.top_out = False
        self.current_tetromino = None
        self.shadow = None

        self.holding = False
        self.held_tetromino = None

    def reset(self):
        """Reset the board."""
        self.__init__()

    def __str__(self):
        """Return cropped version of board."""
        return str(self.board[3:, 3:self.width-3])

    def get_height(self):
        """Return height list of board."""
        return self.fill_height[:, 3:self.width-3]

    def _find_line_clear(self):
        """Locate the rows that have a line clear.

        Returns
        -------
        filled_rows: numpy array of integers
            Contains the rows that have a line clear.
        """
        board = self.board[0:self.height-1:, 3:self.width-3]
        rows = np.where((board == np.ones((1, self.width-6))).all(axis=1))
        filled_rows = rows[0]
        return filled_rows

    def _line_clear_check(self):
        """Check to see if there is a line clear. If there is, delete the rows
        that contain the line clear are deleted.
        """
        self.filled_rows = self._find_line_clear()
        if self.filled_rows.size != 0:
            # Delete the rows that have a line clears.
            self.board = np.delete(self.board, self.filled_rows, axis=0)
            self.fill_height -= self.filled_rows.size

            # Pad the top of the board with rows of 0's.
            npad = ((len(self.filled_rows), 0), (0, 0))
            self.board = np.pad(self.board, pad_width=npad, mode='constant')

            # Adjust heights if needed - special case where the line clear is at
            # the top and there are holes directly beneath the line clear.
            for i in range(3, self.width-3):
                if self.height - max(self.filled_rows) - 2 == self.fill_height[0, i]:
                    while self.board[self.height - self.fill_height[0, i] - 1, i] == 0:
                        self.fill_height[0, i] -= 1

    def _collision(self, tetromino):
        """Check to see if tetromino has collided with a placed tetromino."""
        p = tetromino.block_coordinates()
        if self.board[p[0], p[1]].any() == 1 or self.board[p[0], p[1]].any() == 9:
            return True
        return False

    def update_board(self, new_tetromino, drop=False):
        """Update the state of the board and the tetromino's position. Return
        true if the tetromino is placed, false otherwise."""

        # Erase image of current tetromino (if it exists).
        if self.current_tetromino is not None:
            p = self.current_tetromino.block_coordinates()
            self.board[p[0], p[1]] = 0

        # If the new tetromino has a position that is a collision, place it.
        if self._collision(new_tetromino):
            if self.current_tetromino is None:
                self.top_out = True
                return True
            if drop:
                self.place_tetromino()
                self._line_clear_check()
                new_tetromino.new_shape()
                self.update_board(new_tetromino)
                return True
            else:
                new_tetromino.rotation_index = self.current_tetromino.rotation_index
                new_tetromino.row = self.current_tetromino.row
                new_tetromino.col = self.current_tetromino.col
                self.board[p[0], p[1]] = 1
                return False

        # Find shadow for new tetromino.
        self.shadow = copy.deepcopy(new_tetromino)
        while not self._collision(self.shadow):
            self.shadow.row += 1
        self.shadow.row -= 1

        # Write the new tetromino with its new position onto the board.
        p = new_tetromino.block_coordinates()
        self.board[p[0], p[1]] = 1

        # Save the new tetromino as the current one.
        self.current_tetromino = copy.deepcopy(new_tetromino)

        return False

    def place_tetromino(self):
        """Place the tetromino onto the board."""

        # Integrate tetromino into board & update heights.
        p = self.current_tetromino.block_coordinates()
        self.board[p[0], p[1]] = 1

        for i in np.unique(p[1]):
            self.fill_height[0, i] = np.maximum(
                self.fill_height[0, i],
                self.height - np.min(p[0][np.where(p[1] == i)]) - 1
                )
        self.current_tetromino = None
        self.holding = False

    def hold(self, tetromino):
        """Hold the tetromino."""
        if not self.holding:
            if self.held_tetromino == None:
                self.held_tetromino = Tetromino()
                self.held_tetromino.copy_held(tetromino)
                tetromino.new_shape()
            else:
                temp_tet = copy.deepcopy(self.held_tetromino)
                self.held_tetromino.copy_held(tetromino)
                tetromino.copy_held(temp_tet)
            self.holding = True
            self.update_board(tetromino)


    def rotate_right(self, tetromino):
        """Rotate the tetromino shape right."""
        tetromino.rotation_index = (tetromino.rotation_index + 1)%4
        p = tetromino.block_coordinates()

        # Ensure none of the tetromino's blocks surpass the boundaries when
        # rotating.
        if np.max(p[1]) >= self.right_boundary:
            tetromino.col -= np.max(p[1]) - self.right_boundary
        if np.min(p[1]) <= self.left_boundary:
            tetromino.col += self.left_boundary - np.min(p[1])
        self.update_board(tetromino)

    def rotate_left(self, tetromino):
        """Rotate the tetromino shape left."""
        tetromino.rotation_index = (tetromino.rotation_index - 1)%4
        p = tetromino.block_coordinates()

        # Ensure none of the tetromino's blocks surpass the boundaries when
        # rotating.
        if np.max(p[1]) >= self.right_boundary:
            tetromino.col -= np.max(p[1]) - self.right_boundary
        if np.min(p[1]) <= self.left_boundary:
            tetromino.col += self.left_boundary - np.min(p[1])
        self.update_board(tetromino)

    def move_right(self, tetromino):
        """Move the tetromino to the right."""
        p = tetromino.block_coordinates()
        if np.max(p[1]) >= self.right_boundary:
            return
        tetromino.col += 1
        self.update_board(tetromino)

    def move_left(self, tetromino):
        """Move the tetromino to the left."""
        p = tetromino.block_coordinates()
        if np.min(p[1]) <= self.left_boundary:
            return
        tetromino.col -= 1
        self.update_board(tetromino)

    def soft_drop(self, tetromino):
        """Move the tetromino downwards."""
        tetromino.row += 1
        return self.update_board(tetromino, True)

    def hard_drop(self, tetromino):
        """Instantly drop the tetromino to the bottom of the board."""
        p = tetromino.block_coordinates()
        self.board[p[0], p[1]] = 0
        while not self._collision(tetromino):
            tetromino.row += 1
        tetromino.row -= 1
        self.update_board(tetromino)

    def up(self, tetromino):
        """Move the tetromino upwards."""
        tetromino.row -= 1
        self.update_board(tetromino)


class Tetromino():
    """Class for the Tetrominos in Tetris."""

    COLORS = ['blue', 'red', 'yellow', 'orange', 'cyan', 'purple']

    def __init__(self):
        """Create a random tetromino, set its position, set its left and right
        boundaries.
        """
        # Board dimensions
        self.width = 10 + 6

        # Tetromino position
        self.row = 3
        self.col = self.width//2 - 2

        self.shape = list(SHAPES.keys())[random.randint(0, 6)]
        self.tetromino = SHAPES[self.shape]
        self.rotation_index = 0
        self.color = self.COLORS[random.randint(0,5)]

        self.next_shape = list(SHAPES.keys())[random.randint(0, 6)]
        self.next_tetromino = SHAPES[self.next_shape]
        self.next_color = self.COLORS[random.randint(0,5)]

    def reset(self):
        """Reset the tetromino."""
        self.__init__()

    def copy_held(self, tetromino):
        self.row = 3
        self.col = int(self.width/2)-2
        self.shape = tetromino.shape
        self.rotation_index = 0
        self.color = tetromino.color
        self.tetromino = SHAPES[self.shape]

    def current_tetromino(self):
        """Return numpy array of tetromino matrix"""
        return self.tetromino[self.rotation_index]

    def new_shape(self):
        """Randomly generate new shape."""
        self.row = 3
        self.col = self.width//2 - 2
        self.shape = self.next_shape
        self.tetromino = copy.deepcopy(self.next_tetromino)
        self.color = self.next_color
        self.rotation_index = 0

        self.next_shape = list(SHAPES.keys())[random.randint(0, 6)]
        self.next_tetromino = SHAPES[self.next_shape]
        self.next_color = self.COLORS[random.randint(0,5)]

    def position(self):
        """Return the position of the tetromino as tuple."""
        return (self.row, self.col)

    def next_block_coordinates(self):
        """Return the coordinates for every block in the tetromino matrix.

        Returns a tuple of a pair of np arrays. The first array contains the
        rows and the second array contains columns.
        """
        rows = np.where(self.next_tetromino[0] == 1)[0]
        cols = np.where(self.next_tetromino[0] == 1)[1]
        return (rows, cols)

    def block_coordinates(self):
        """Return the coordinates for every block in the tetromino matrix
        relavtive to the tetris board.

        Returns a tuple of a pair of np arrays. The first array contains the
        rows and the second array contains columns.
        """
        rows = np.where(self.tetromino[self.rotation_index] == 1)[0] + self.row
        cols = np.where(self.tetromino[self.rotation_index] == 1)[1] + self.col
        return (rows, cols)


class Score:
    LC_SCORE = {
        1 : 40,
        2 : 100,
        3 : 300,
        4 : 1200
    }

    def __init__(self):
        self.score = 0
        self.line_count = 0
        self.level = 0

    def add_score(self, line_clears):
        self.score += self.LC_SCORE[line_clears]*(self.level+1)
        self.line_count += line_clears
        if self.level != 10:
            if self.line_count >= 10:
                self.line_count = 0
                self.level += 1
                return True

    def reset(self):
        self.score = 0
        self.line_count = 0
        self.level = 0
