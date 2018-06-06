
import random
import numpy as np
from ..utils.shapes import SHAPES


TETROMINO_NAMES = list(SHAPES.keys())


class Tetromino:
    """Class for the Tetrominos in Tetris."""

    def __init__(self, grid_width=10):
        """Create a random tetromino, set its position, set its left and right
        boundaries.

        Parameters
        ----------
        grid_width: integer (default=10)
            Specifies the width of the Tetris grid being used.
        """
        self.tetromino = SHAPES[TETROMINO_NAMES[random.randint(0, 6)]]
        self.rotation_index = 0

        # Calculate position and left and right boundaries.
        # Tetris board is padded with three extra columns on both sides of
        # the grid.
        self.row = 0
        self.col = 3+ int(grid_width/2 - 2)
        self.left_boundary = 2
        self.right_boundary = grid_width + 3
        self.grid_width = grid_width

    def new_shape(self):
        """Randomly generate new shape."""
        self.__init__(self.grid_width)

    def shape(self):
        """Return numpy array of tetromino matrix"""
        return self.tetromino[self.rotation_index]

    def rotate(self):
        """Rotate the tetromino shape.

        Rotation is done by cycling through the rotation_index shapes obtained
        from shapes.py
        """
        self.rotation_index = (self.rotation_index + 1)%4
        indices = np.where(self.tetromino[self.rotation_index] > 0)

        # Ensure none of the tetromino's blocks surpass the boundaries.
        for i in range(indices[0].size):
            while (self.col + indices[1][i]) >= self.right_boundary:
                self.col -= 1
            while (self.col + indices[1][i]) <= self.left_boundary:
                self.col += 1

    def move_right(self):
        """Move the tetromino to the right. Before rotation is done, ensure that
        the position is valid.
        """
        for point in self.block_coordinates():
            if (point[1]) >= self.right_boundary - 1:
                return

        self.col += 1

    def move_left(self):
        """Move the tetromino to the left. Before rotation is done, ensure that
        the position is valid.
        """
        for point in self.block_coordinates():
            if (point[1]) <= self.left_boundary + 1:
                return

        self.col -= 1

    def move_down(self):
        """Move the tetromino downwards."""
        self.row += 1

    def position(self):
        """Return the position of the tetromino as tuple."""
        return (row, col)

    def block_coordinates(self):
        """Return the coordinates for every block in the tetromino matrix.

        Returns
        -------
        coordinates: list of integer lists
            The lists contain coordinate pairs that specifiy the row and column
            each tetromino's block relative to the grid.
        """
        coordinates = []

        # Locate which indices contain a block (1).
        indices = np.where(self.tetromino[self.rotation_index] == 1)

        # Format coordinates into a list of tuples.
        for i in range(indices[0].size):
            coordinates.append((self.row + indices[0][i],
                                self.col + indices[1][i]))

        return coordinates
