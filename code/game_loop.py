import pygame

from player import Player
from tile import Tile, TileManager
from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window
        self.__tile_manager = TileManager()

        self.player = Player()
        self.t = Tile(pygame.Vector2(10, 100), "block")

        self.__running = True

    def __event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if event.type == pygame.WINDOWDISPLAYCHANGED:
                self.__window.update_size()

    def __update(self) -> None:
        delta = self.__window.update_clock() * 0.01
        self.player.update(delta)

    def __draw(self) -> None:
        self.__window.clear(pygame.Color("#232332"))
        self.__tile_manager.draw_tile(self.__window.surface, self.t)
        self.player.draw(self.__window.surface)
        pygame.display.update()

    def start(self) -> None:
        while self.__running:
            self.__update()
            self.__draw()
            self.__event_loop()

        pygame.quit()
