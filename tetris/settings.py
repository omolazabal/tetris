
"""All available settings for Tetris game"""

class Keyboard:
    def __init__(self):
        self.delay = 20
        self.interval = 20

class Display:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.fps = 60

class Board:
    def __init__(self):
        pass

class Tetromino:
    def __init__(self):
        self.speed = 1000

class PrelaunchSettings:
    keyboard = Keyboard()
    display = Display()
    board = Board()
    tetromino = Tetromino()

