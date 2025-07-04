from pygame import init

from window import Window
from game_loop import GameLoop

def main() -> None:
    init()

    window_size = (1000, 600)
    window_fps = 60
    window_caption = "PyDash"
    window = Window(window_size, window_fps)
    window.set_caption(window_caption)
    window.set_icon("../resources/icon.png")

    game_loop = GameLoop(window)
    game_loop.start()

if __name__ == "__main__":
    main()
