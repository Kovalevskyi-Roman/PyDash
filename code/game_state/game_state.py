import pygame


class GameState:
    name: str = "game_state"

    def __init__(self, *args, **kwargs) -> None:
        self.__window_size = pygame.display.get_window_size()

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()

    def update(self, delta_time: float, *args, **kwargs) -> str:
        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        pass
