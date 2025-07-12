import pygame

from player import Player


class Camera:
    def __init__(self, player: Player, window_size: tuple[int, int]) -> None:
        self.__player = player
        self.window_size = window_size
        self.half_win_size = (self.window_size[0] / 2, self.window_size[1] / 2)
        self.scroll = pygame.Vector2(0, 0)
        self.scroll_smooth = 20

        self.set_scroll()

    def update_scroll(self) -> None:
        self.scroll.x += (self.__player.rect.x - self.scroll.x - self.half_win_size[0]) / self.scroll_smooth
        self.scroll.y += (self.__player.rect.y - self.scroll.y - self.half_win_size[1] - 40) / self.scroll_smooth

    def set_scroll(self) -> None:
        self.scroll.x = self.__player.rect.x - self.half_win_size[0]
        self.scroll.y = self.__player.rect.y - self.half_win_size[1] - 40

    def update_window_size(self) -> None:
        self.window_size = pygame.display.get_window_size()
        self.half_win_size = (self.window_size[0] / 2, self.window_size[1] / 2)
        self.set_scroll()

    def draw(self, surface: pygame.Surface) -> None:
        self.__player.draw(surface, self.scroll)
