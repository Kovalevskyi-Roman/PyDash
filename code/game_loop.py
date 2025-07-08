import pygame

from camera import Camera
from collider import Collider
from level import Level
from player import Player
from tile import Tile, TileManager
from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window
        self.__tile_manager = TileManager()

        self.player = Player()
        self.camera = Camera(self.player, self.__window.size)
        self.level = Level("level", self.__tile_manager, self.__window.size)
        self.collider = Collider(self.player, self.level, self.__window.size)

        self.level.save()

        self.__running = True

    def __event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if event.type == pygame.WINDOWRESIZED:
                self.__window.update_size()
                self.camera.update_window_size()
                self.level.update_window_size()
                self.collider.update_window_size()

    def __update(self) -> None:
        delta = self.__window.update_clock() * 0.01
        self.player.update(delta)
        self.camera.update_scroll()
        self.collider.check_collision(delta, self.camera.scroll)

    def __draw(self) -> None:
        self.__window.clear(pygame.Color("#232332"))
        self.level.draw(self.__window.surface, self.camera.scroll)
        self.camera.draw(self.__window.surface)
        pygame.display.update()

    def start(self) -> None:
        while self.__running:
            self.__update()
            self.__draw()
            self.__event_loop()

        pygame.quit()
