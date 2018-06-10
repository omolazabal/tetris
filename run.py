
from tetris import game


def main():
    Tetris = game.Game()
    Tetris.settings.display.fps = 30
    Tetris.debug = True
    Tetris.start()

if __name__ == "__main__":
    main()
