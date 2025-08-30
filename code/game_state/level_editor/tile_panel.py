import pygame

from tile import TileManager


class TilePanel:
    def __init__(self, tile_manager: TileManager) -> None:
        self.__tile_manager = tile_manager
        self.__window_size = pygame.display.get_window_size()
        self.__tiles: dict[str, pygame.Surface] = self.__tile_manager.get_tile_textures()
        self.selected_tile = list(self.__tiles.keys())[0]

        self.__selection = pygame.Surface([32, 32])
        self.__selection.fill("#22FF22")
        self.__selection.set_alpha(100)

        self.y_pos = self.__window_size[1] // 1.2  # then smaller then lower

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.y_pos = self.__window_size[1] // 1.2

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "gray", [0, self.y_pos, self.__window_size[0], self.__window_size[1] - self.y_pos])

        x = 10
        y = 10
        for key, texture in self.__tiles.items():
            surface.blit(pygame.transform.scale(texture, [24, 24]), [x, y + self.y_pos])

            if key == self.selected_tile:
                surface.blit(self.__selection, [x - 4, y + self.y_pos - 4])
                pygame.draw.rect(surface, "#22AA22", [x - 4, y + self.y_pos - 4, 32, 32], 2)

            x += 34
            if x + 34 >= self.__window_size[0]:
                x = 10
                y += 34

    def update(self) -> None:
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        x = 10
        y = 10
        for key in self.__tiles.keys():
            if not pygame.Rect(x, y + self.y_pos, 24, 24).collidepoint(mouse_pos) or not mouse_press[0]:
                x += 34
                if x + 34 >= self.__window_size[0]:
                    x = 10
                    y += 34
                continue

            self.selected_tile = key
            break
