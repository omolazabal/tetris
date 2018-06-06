
import numpy as np
from . import tetromino
import copy


class Grid():
    """Class for the grid in Tetris."""

    def __init__(self, grid_width=10, grid_height=20):
        """Set the settings for the Tetris grid. This includes the width,
        height, and initial cell values.

        Parameters
        ----------
        grid_width: integer (default=10)
            Width of the Tetris grid.
        grid_height: integer (default=20)
            Height of the Tetris grid.

        """
        self.width = grid_width
        self.height = grid_height + 3  # Accommodate for spawning area.
        self.grid = np.zeros((self.height, self.width + 6), dtype=int)
        self.grid[self.height-1, :] = np.ones(self.width + 6)
        self.current_tetromino = None
        self.top_out = False

    def new_grid(self):
        """Clear the grid."""
        self.__init__()

    def _find_line_clear(self):
        """Locate the rows that have a line clear.

        Returns
        -------
        filled_rows: numpy array of integers
            Contains the rows that have a line clear.
        """
        grid = self.grid[0:self.height-1:, 3:self.width+3]
        rows = np.where((grid == np.ones((1, self.width))).all(axis=1))
        filled_rows = rows[0]
        return filled_rows

    def _line_clear_check(self):
        """Check to see if there is a line clear. If there is, delete the rows
        that contain the line clear are deleted.
        """
        filled_rows = self._find_line_clear()
        if filled_rows.size != 0:
            # Delete the rows that have a line clears.
            self.grid = np.delete(self.grid, filled_rows, axis=0)

            # Pad the top of the grid with rows of 0's.
            npad = ((len(filled_rows), 0), (0, 0))
            self.grid = np.pad(self.grid, pad_width=npad, mode='constant')

    def collision(self, tetromino):
        """Check to see if tetromino has collided with a placed tetromino."""
        for point in tetromino.block_coordinates():
            if self.grid[point[0], point[1]] == 1:
                return True

        return False

    def update_grid(self, new_tetromino):
        """Update the state of the grid and the tetromino's position. Return
        true if the tetromino is placed, false otherwise."""

        # Erase image of current tetromino (if it exists).
        if self.current_tetromino is not None:
            for point in self.current_tetromino.block_coordinates():
                self.grid[point[0], point[1]] = 0

        # If the new tetromino has a position that is a collision, place it.
        if self.collision(new_tetromino):
            self.place_tetromino()
            self._line_clear_check()
            if self.top_out:
                self.new_grid()
            return True

        # Write the new tetromino with its new position onto the grid.
        for point in new_tetromino.block_coordinates():
            self.grid[point[0], point[1]] = 1

        # Save the new tetromino as the current one.
        self.current_tetromino = copy.deepcopy(new_tetromino)

        return False

    def place_tetromino(self):
        """Place the tetromino onto the grid."""

        # Top out occurs when a new tetromino has a collision immediately when
        # it spawns (before theres a chance to save it as the "current"
        # tetromino.
        if self.current_tetromino == None:
            self.top_out = True
        else:
            # Integrate tetromino into grid
            for point in self.current_tetromino.block_coordinates():
                self.grid[point[0], point[1]] = 1
            self.current_tetromino = None
