
from tetris import tetris


def main():
    Tetris = tetris.Game()

    Tetris.set_grid_dim((10,20))
    Tetris.set_screen_dim((640,480))
    Tetris.set_key_repeat_delay(150)
    Tetris.set_key_repeat_interval(30)

    Tetris.play()

if __name__ == "__main__":
    main()
