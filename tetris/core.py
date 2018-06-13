
import random
import numpy as np
import copy
from tetris.utils import SHAPES


class Board:
    """Class for the board in Tetris."""

    def __init__(self):
        """Set the settings for the Tetris board. This includes the width,
        height, and initial cell values.
        """
        self.width = 10 + 6   # Accommodate for sides.
        self.height = 20 + 4  # Accommodate for base and spawn.
        self.fill_height = np.zeros((1, self.width), dtype=int)
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.board[self.height-1, :] = np.ones(self.width)*9
        self.filled_rows = np.array([])

        self.top_out = False
        self.current_tetromino = None
        self.shadow = None

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

    def hard_drop(self, tet):
        """Instantly drop the tetromino to the bottom of the board."""
        p = tet.block_coordinates()
        self.board[p[0], p[1]] = 0
        while not self.collision(tet):
            tet.soft_drop()
        tet.up()

    def collision(self, tet):
        """Check to see if tetromino has collided with a placed tetromino."""
        p = tet.block_coordinates()
        if self.board[p[0], p[1]].any() == 1 or self.board[p[0], p[1]].any() == 9:
            return True
        return False

    def update_board(self, new_tetromino):
        """Update the state of the board and the tetromino's position. Return
        true if the tetromino is placed, false otherwise."""

        # Erase image of current tetromino (if it exists).
        if self.current_tetromino is not None:
            p = self.current_tetromino.block_coordinates()
            self.board[p[0], p[1]] = 0

        # If the new tetromino has a position that is a collision, place it.
        if self.collision(new_tetromino):
            self.place_tetromino()
            self._line_clear_check()
            return True

        # Find shadow for new tetromino.
        self.shadow = copy.deepcopy(new_tetromino)
        self.hard_drop(self.shadow)

        # Write the new tetromino with its new position onto the board.
        p = new_tetromino.block_coordinates()
        self.board[p[0], p[1]] = 1

        # Save the new tetromino as the current one.
        self.current_tetromino = copy.deepcopy(new_tetromino)

        return False

    def place_tetromino(self):
        """Place the tetromino onto the board."""

        # Top out occurs when a new tetromino has a collision immediately when
        # it spawns (before theres a chance to save it as the "current"
        # tetromino.
        if self.current_tetromino == None:
            self.top_out = True
        else:
            # Integrate tetromino into board & update heights.
            p = self.current_tetromino.block_coordinates()
            self.board[p[0], p[1]] = 1

            for i in np.unique(p[1]):
                self.fill_height[0, i] = np.maximum(
                    self.fill_height[0, i],
                    self.height - np.min(p[0][np.where(p[1] == i)]) - 1
                    )
            self.current_tetromino = None


class Tetromino():
    """Class for the Tetrominos in Tetris."""

    COLORS = ['blue', 'red', 'yellow', 'orange', 'cyan', 'purple']

    def __init__(self):
        """Create a random tetromino, set its position, set its left and right
        boundaries.
        """
        # Board dimensions
        self.width = 10 + 6
        self.height = 20 + 4
        self.left_boundary = 3
        self.right_boundary = self.width - 4

        # Tetromino position
        self.row = 0
        self.col = int(self.width/2) - 2

        self.shape = list(SHAPES.keys())[random.randint(0, 6)]
        self.tetromino = SHAPES[self.shape]
        self.rotation_index = 0
        self.held_tet = None
        self.holding = False
        self.color = self.COLORS[random.randint(0,5)]

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
        self.color = self.COLORS[random.randint(0,5)]

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


class Score:
    pass
