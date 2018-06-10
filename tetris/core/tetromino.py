
import random
import copy
import numpy as np
from ..utils.shapes import SHAPES
from .board import Board


class Tetromino(Board):
    """Class for the Tetrominos in Tetris."""

    def __init__(self):
        """Create a random tetromino, set its position, set its left and right
        boundaries.

        Parameters
        ----------
        board_width: integer (default=10)
            Specifies the width of the Tetris board being used.
        """
        self.shape = list(SHAPES.keys())[random.randint(0, 6)]
        self.tetromino = SHAPES[self.shape]
        self.rotation_index = 0
        self.held_tet = None
        self.holding = False

        # Accomodate for padding of board and tetromino pieces.
        self.row = 0
        self.col = int(self.width/2) - 2
        self.left_boundary = 3
        self.right_boundary = self.width - 4

    def reset(self):
        """Reset the tetromino."""
        self.__init__()

    def current_tetromino(self):
        """Return numpy array of tetromino matrix"""
        return self.tetromino[self.rotation_index]

    def new_shape(self):
        """Randomly generate new shape."""
        self.shape = list(SHAPES.keys())[random.randint(0, 6)]
        self.tetromino = SHAPES[self.shape]
        self.rotation_index = 0
        self.holding = False

        self.row = 0
        self.col = int(self.width/2) - 2

    def held_tetromino(self):
        """Return the tetromino that is being held."""
        if self.held_tet == None:
            return np.zeros((4, 4), dtype=int)
        return self.held_tet[0]

    def hold(self):
        """Hold the tetromino."""
        if not self.holding:
            if self.held_tet == None:
                self.held_tet = copy.deepcopy(self.tetromino)
                self.new_shape()
            else:
                temp_tet = copy.deepcopy(self.held_tet)
                self.held_tet = copy.deepcopy(self.tetromino)
                self.tetromino = copy.deepcopy(temp_tet)
            self.holding = True


    def rotate_right(self):
        """Rotate the tetromino shape right.

        Rotation is done by cycling through the rotation_index shapes obtained
        from shapes.py
        """
        self.rotation_index = (self.rotation_index + 1)%4
        p = self.block_coordinates()

        # Ensure none of the tetromino's blocks surpass the boundaries when
        # rotating.
        if np.max(p[1]) >= self.right_boundary:
            self.col -= np.max(p[1]) - self.right_boundary
        if np.min(p[1]) <= self.left_boundary:
            self.col += self.left_boundary - np.min(p[1])

    def rotate_left(self):
        """Rotate the tetromino shape left.

        Rotation is done by cycling through the rotation_index shapes obtained
        from shapes.py
        """
        self.rotation_index = (self.rotation_index - 1)%4
        p = self.block_coordinates()

        # Ensure none of the tetromino's blocks surpass the boundaries when
        # rotating.
        if np.max(p[1]) >= self.right_boundary:
            self.col -= np.max(p[1]) - self.right_boundary
        if np.min(p[1]) <= self.left_boundary:
            self.col += self.left_boundary - np.min(p[1])

    def move_right(self):
        """Move the tetromino to the right. Before rotation is done, ensure that
        the position is valid.
        """
        p = self.block_coordinates()
        if np.max(p[1]) >= self.right_boundary:
            return

        self.col += 1

    def move_left(self):
        """Move the tetromino to the left. Before rotation is done, ensure that
        the position is valid.
        """
        p = self.block_coordinates()
        if np.min(p[1]) <= self.left_boundary:
            return

        self.col -= 1

    def up(self):
        """Move the tetromino upwards."""
        self.row -= 1

    def soft_drop(self):
        """Move the tetromino downwards."""
        self.row += 1

    def hard_drop(self):
        """Instantly drop the tetromino to the bottom of the board."""
        p = self.block_coordinates()
        self.row += np.min((self.height - p[0]) - self.fill_height[0, p[1]]) - 2

    def position(self):
        """Return the position of the tetromino as tuple."""
        return (self.row, self.col)

    def block_coordinates(self):
        """Return the coordinates for every block in the tetromino matrix.

        Returns a tuple of a pair of np arrays. The first array contains the
        rows and the second array contains columns.
        """
        rows = np.where(self.tetromino[self.rotation_index] == 1)[0] + self.row
        cols = np.where(self.tetromino[self.rotation_index] == 1)[1] + self.col
        return (rows, cols)
