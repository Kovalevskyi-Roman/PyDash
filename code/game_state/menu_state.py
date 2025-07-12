import pygame

from .game_state import GameState


class Menu(GameState):
    name = "menu"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        # play button
        self.__play_btn_texture = pygame.image.load("../resources/textures/gui/play_button.png").convert_alpha()
        self.__play_btn_texture = pygame.transform.scale_by(self.__play_btn_texture, 2)
        self.__play_btn_rect = self.__play_btn_texture.get_rect(
            x=self.__window_size[0] // 2 - 40, y=self.__window_size[1] // 3
        )

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.__play_btn_rect.x = self.__window_size[0] // 2 - 40
        self.__play_btn_rect.y = self.__window_size[1] // 3

    def update(self, delta_time: float, *args, **kwargs) -> str:
        mouse_pos = pygame.mouse.get_pos()

        if self.__play_btn_rect.collidepoint(mouse_pos) and pygame.mouse.get_just_pressed()[0]:
            return "level_list"

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.blit(self.__play_btn_texture, self.__play_btn_rect)
