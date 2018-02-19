
import numpy as np
import random
from shapes import SHAPES

TETROMINO_NAMES = list(SHAPES.keys())

class Tetromino:
    def __init__(self, grid_width=10):
        """Create a random tetromino and set its coordinates left and right
        boundaries.

        The shapes are obtained from shapes.py. The origin of each shape is
        the top left corner (0, 0) of their matrix.

        Keyword arguments:
        grid_width -- specifies the width of the Tetris grid being used
                      (default 10).

        Instance variables:
        name -- Name of the tetromino being used.
        tetromino -- Shape matrix of the tetromino being used.
        shape_type -- Rotation of the tetromino is being used.
        coordinate -- Coordinate of tetromino on the Tetris grid.
        left_boundary -- Column a tetromino block's position cannot be less
                         less than or equal to.
        right_boundary -- Column a tetromino block's position cannot be greater
                          than or equal to.
        """
        self.name = TETROMINO_NAMES[random.randint(0, 6)]
        self.tetromino = SHAPES[self.name]
        self.shape_type = 0

        # Calculate coordinate and left and right boundaries noting that the
        # Tetris board is padded with three extra columns on both sides of
        # the grid.
        self.coordinate = [0, 3 + int(grid_width/2 - 2)]  # Center of grid.
        self.left_boundary = 2
        self.right_boundary = grid_width + 3
        self.grid_width = grid_width

    def new_shape(self):
        """Randomly generate new shape using __init__ constructor."""
        self.__init__(self.grid_width)

    def shape(self):
        """Return the matrix shape of the tetromino."""
        return self.tetromino[self.shape_type]

    def rotate(self):
        """Rotate the tetromino shape.

        Rotation is done by cycling through the rotation shapes obtained from
        shapes.py. After a rotation has been performed, a check is done
        ensuring that none of the tetromino's block coordinates are pass the
        boundaries. If they are, the tetromino is shifted away from the
        boundary until all blocks are within the boundaries.
        """
        self.shape_type = (self.shape_type + 1)%4

        # Iterate through each of the tetromino's block coordinates.
        for point in self.block_coordinates():
            # Check if the block's coordinate is beyond or on the boundaries.
            while (self.coordinate[1] + point[1]) >= self.right_boundary:
                self.coordinate[1] -= 1
            while (self.coordinate[1] + point[1]) <= self.left_boundary:
                self.coordinate[1] += 1

    def move_right(self):
        """Move the tetromino to the right. Before rotation is done, ensure that
        the coordinate is valid.
        """
        # Iterate through each of the tetromino's block coordinates.
        for point in self.block_coordinates():
            # Check if the block's coordinate is beyond or on the boundary.
            if (self.coordinate[1] + point[1]) >= self.right_boundary - 1:
                return  # Don't perform shift.

        self.coordinate[1] += 1  # Shift

    def move_left(self):
        """Move the tetromino to the left. Before rotation is done, ensure that
        the coordinate is valid.
        """
        # Iterate through each of the tetromino's block coordinates.
        for point in self.block_coordinates():
            # Check if the block's coordinate is beyond or on the boundary.
            if (self.coordinate[1] + point[1]) <= self.left_boundary + 1:
                return  # Don't perform shift.

        self.coordinate[1] -= 1  # Shift

    def move_down(self):
        """Move the tetromino downwards."""
        self.coordinate[0] += 1

    def position(self):
        """Return the coordinates of the tetromino in a tuple."""
        return tuple(self.coordinate)

    def block_coordinates(self):
        """Return the coordinates for every block in the tetromino matrix.

        Coordinates are obtained by first obtaining the indices of where in
        the shape matrix contains a value that is greater than 0. Those indices
        are then formatted into tuples and appended onto a list.
        """
        coordinates = []

        # Locate which indices contain a block (1).
        indices = np.where(self.tetromino[self.shape_type] > 0)

        # Format coordinates into a list of tuples.
        for i in range(indices[0].size):
            coordinates.append((indices[0][i], indices[1][i]))

        return coordinates

