
"""All available settings for Tetris game"""

class KeyboardSettings:
    delay = 150
    interval = 30

class TetrominoSettings:
    tile_size = 16

class DisplaySettings:
    width = TetrominoSettings.tile_size*27
    height = TetrominoSettings.tile_size*25
    fps = 60

class BoardSettings:
    pass

class TimerSettings:
    drop_interval = 1000
