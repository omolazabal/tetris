
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
        self.height = grid_height + 4  # Accommodate for spawning area & base.
        self.grid = np.zeros((self.height, self.width + 6), dtype=int)
        self.grid[self.height-1, :] = np.ones(self.width + 6)*9
        self.current_tetromino = None
        self.ghost = None
        self.top_out = False
        self.fill_height = np.zeros((1, self.width + 6), dtype=int)
        self.fill_height.reshape(1, self.width+6, 1)

    def new_grid(self):
        """Clear the grid."""
        self.__init__()

    def get_grid(self):
        """Return cropped version of grid."""
        return self.grid[3:, 3:self.width+3]

    def get_height(self):
        """Return height list of grid."""
        return self.fill_height[:, 3:self.width + 3]

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
            self.fill_height -= filled_rows.size

            # Pad the top of the grid with rows of 0's.
            npad = ((len(filled_rows), 0), (0, 0))
            self.grid = np.pad(self.grid, pad_width=npad, mode='constant')

            # Adjust heights if needed - special case where the line clear is at
            # the top and there are holes directly beneath the line clear.
            for i in range(3, self.width+3):
                if self.height - max(filled_rows) - 2 == self.fill_height[0, i]:
                    while self.grid[self.height - self.fill_height[0, i] - 1, i] == 0:
                        self.fill_height[0, i] -= 1

    def collision(self, tetromino):
        """Check to see if tetromino has collided with a placed tetromino."""
        for p in tetromino.block_coordinates():
            if self.grid[p[0], p[1]] == 1 or self.grid[p[0] ,p[1]] == 9:
                return True

        return False

    def update_grid(self, new_tetromino):
        """Update the state of the grid and the tetromino's position. Return
        true if the tetromino is placed, false otherwise."""

        # Erase image of current tetromino (if it exists).
        if self.current_tetromino is not None:
            for p, gp in zip(self.current_tetromino.block_coordinates(),
                             self.ghost.block_coordinates()):
                self.grid[gp[0], gp[1]] = 0
                self.grid[p[0], p[1]] = 0

        # If the new tetromino has a position that is a collision, place it.
        if self.collision(new_tetromino):
            self.place_tetromino()
            self._line_clear_check()
            if self.top_out:
                self.new_grid()
            return True

        # Find ghost for new tetromino.
        self.ghost = copy.deepcopy(new_tetromino)
        while not self.collision(self.ghost):
            self.ghost.drop()
        self.ghost.up()

        # Write the new tetromino with its new position onto the grid.
        for p, gp in zip(new_tetromino.block_coordinates(),
                         self.ghost.block_coordinates()):
            self.grid[gp[0], gp[1]] = 2
            self.grid[p[0], p[1]] = 1

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
            # Integrate tetromino into grid & update heights.
            for point in self.current_tetromino.block_coordinates():
                self.grid[point[0], point[1]] = 1
                self.fill_height[0, point[1]] = max(
                        self.fill_height[0, point[1]], self.height-point[0] - 1)
            self.current_tetromino = None
