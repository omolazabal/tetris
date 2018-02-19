
import numpy as np
import tetromino
import copy


class Grid():
    def __init__(self, grid_width=10, grid_height=20):
        """Set the width and height of the Tetris grid.

        Keyword arguments:
        grid_width -- Width of the Tetris grid (default 10)
        grid_height -- Height of the Tetris grid (default 20)

        Instance variables:

        """
        self.width = grid_width
        self.height = grid_height + 3  # Accommodate for spawning area (3 spaces)

        self.grid = np.zeros((self.height, self.width + 6), dtype=int)
        self.grid[self.height-1, :] = np.ones(self.width + 6)

        self.current_tetromino = None
        self.top_out = False

    def new_grid(self):
        self.__init__()
        return

    def find_line_clear(self):
        # Find rows that are filled.
        grid = self.grid[0:self.height-1:, 3:self.width+3]
        rows = np.where((grid == np.ones((1, self.width))).all(axis=1))
        return rows[0]

    def clear_line_check(self):
        rows = self.find_line_clear()
        if rows.size != 0:
            # Delete the rows that have a line clears.
            self.grid = np.delete(self.grid, rows, axis=0)

            # Pad the top of the grid with rows of 0's.
            npad = ((len(rows), 0), (0, 0))
            self.grid = np.pad(self.grid, pad_width=npad, mode='constant')

    def collision(self, tetromino):
        new_position = tetromino.position()

        for point in tetromino.block_coordinates():
            if self.grid[new_position[0] + point[0], new_position[1] + point[1]] == 1:
                return True

        return False

    def update_grid(self, new_teromino):
        if self.current_tetromino is not None:
            # Erase image of current tetromino.
            current_position = self.current_tetromino.position()
            for point in self.current_tetromino.block_coordinates():
                self.grid[current_position[0] + point[0], current_position[1] + point[1]] = 0

        if self.collision(new_teromino):
            self.place_tetromino()
            return True

        # Write the new tetromino with its new position onto the grid.
        new_position = new_teromino.position()
        for point in new_teromino.block_coordinates():
            self.grid[new_position[0] + point[0], new_position[1] + point[1]] = 1

        # Save the new tetromino as the current one.
        self.current_tetromino = copy.deepcopy(new_teromino)

        return False  # Haven't updated grid just yet.

    def place_tetromino(self):
        if self.current_tetromino == None:
            self.top_out = True

        else:
            position = self.current_tetromino.position()

            for point in self.current_tetromino.block_coordinates():
                self.grid[position[0] + point[0], position[1] + point[1]] = 1

            self.current_tetromino = None

    def top_out_occured(self):
        return self.top_out





















