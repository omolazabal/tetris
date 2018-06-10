
"""All available settings for Tetris game"""
class Keyboard:
    def __init__(self):
        self.key_repeat_delay = 150
        self.key_repeat_interval = 30

class Display:
    def __init__(self):
        self.width = 468
        self.height = 60
        self.fps = 30

class Board:
    def __init__(self):
        pass

class Tetromino:
    def __init__(self):
        self.speed = 1000

class Settings:
    keyboard = Keyboard()
    display = Display()
    board = Board()
    tetromino = Tetromino()

