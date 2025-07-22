import pygame

from button import Button
from .game_state import GameState


class Menu(GameState):
    name = "menu"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        self.__play_btn = Button(
            (self.__window_size[0] // 2 - 40, self.__window_size[1] // 3, 80, 80),
            "",
            "../resources/textures/gui/play_button.png",
            2
        )

        self.__settings_btn = Button(
            (self.__window_size[0] // 2 + 80, self.__window_size[1] // 3, 80, 80),
            "",
            "../resources/textures/gui/edit_button.png",
            2
        )

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.__play_btn.rect.topleft = (self.__window_size[0] // 2 - 40, self.__window_size[1] // 3)
        self.__settings_btn.rect.topleft = (self.__window_size[0] // 2 + 80, self.__window_size[1] // 3)

    def update(self, delta_time: float, *args, **kwargs) -> str:
        if self.__play_btn.is_pressed(0):
            return "level_list"

        if self.__settings_btn.is_pressed(0):
            return "settings"

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__play_btn.draw(surface)
        self.__settings_btn.draw(surface)
