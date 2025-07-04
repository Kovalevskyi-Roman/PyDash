import pygame

from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window

        self.__running = True

    def __event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if event.type == pygame.WINDOWDISPLAYCHANGED:
                self.__window.update_size()

    def __update(self) -> None:
        self.__window.update_clock()

    def __draw(self) -> None:
        self.__window.clear(pygame.Color("#232332"))
        pygame.display.update()

    def start(self) -> None:
        while self.__running:
            self.__update()
            self.__draw()
            self.__event_loop()

        pygame.quit()
