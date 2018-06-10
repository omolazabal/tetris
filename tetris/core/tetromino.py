
import random
import numpy as np
from ..utils.shapes import SHAPES


class Tetromino:
    """Class for the Tetrominos in Tetris."""

    def __init__(self, board_width=10):
        """Create a random tetromino, set its position, set its left and right
        boundaries.

        Parameters
        ----------
        board_width: integer (default=10)
            Specifies the width of the Tetris board being used.
        """
        self.tetromino = SHAPES[list(SHAPES.keys())[random.randint(0, 6)]]
        self.rotation_index = 0

        # Calculate position and left and right boundaries.
        # Tetris board is padded with three extra columns on both sides of
        # the board.
        self.row = 0
        self.col = 3 + int(board_width/2 - 2)
        self.left_boundary = 3
        self.right_boundary = board_width + 2
        self.board_width = board_width

    def __str__(self):
        """Return numpy array of tetromino matrix"""
        return str(self.tetromino[self.rotation_index])

    def new_shape(self):
        """Randomly generate new shape."""
        self.__init__(self.board_width)

    def rotate(self):
        """Rotate the tetromino shape.

        Rotation is done by cycling through the rotation_index shapes obtained
        from shapes.py
        """
        self.rotation_index = (self.rotation_index + 1)%4
        indices = self.block_coordinates()

        # Ensure none of the tetromino's blocks surpass the boundaries when
        # rotating.
        if np.max(indices[1]) >= self.right_boundary:
            self.col -= np.max(indices[1]) - self.right_boundary
        if np.min(indices[1]) <= self.left_boundary:
            self.col += self.left_boundary - np.min(indices[1])

    def move_right(self):
        """Move the tetromino to the right. Before rotation is done, ensure that
        the position is valid.
        """
        indices = self.block_coordinates()
        if np.max(indices[1]) >= self.right_boundary:
            return

        self.col += 1

    def move_left(self):
        """Move the tetromino to the left. Before rotation is done, ensure that
        the position is valid.
        """
        indices = self.block_coordinates()
        if np.min(indices[1]) <= self.left_boundary:
            return

        self.col -= 1

    def up(self):
        """Move the tetromino upwards."""
        self.row -= 1

    def soft_drop(self):
        """Move the tetromino downwards."""
        self.row += 1

    def hard_drop(self_height):
        pass

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
