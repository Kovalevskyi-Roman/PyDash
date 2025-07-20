import pygame

from level import Level
from player import Player


class Collider:
    def __init__(self, player: Player, level: Level, window_size: tuple[int, int]) -> None:
        self.__player = player
        self.__level = level
        self.__window_size = window_size

    def set_level(self, new_level: Level) -> None:
        self.__level = new_level

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()

    def __get_collided_tiles(self, scroll: pygame.Vector2) -> tuple[list, list]:
        collided_tiles = []
        tiles = []

        for i in range(len(self.__level.tiles)):
            tile = self.__level.tiles[i]

            if 0 < tile.position.x - scroll.x < self.__window_size[0] and \
                    0 < tile.position.y - scroll.y < self.__window_size[1]:

                tile_rect = pygame.Rect(tile.position.x + tile.hit_box.x, tile.position.y + tile.hit_box.y,
                                        tile.hit_box.width, tile.hit_box.height)

                if self.__player.rect.colliderect(tile_rect):
                    collided_tiles.append(tile_rect)
                    tiles.append(tile)

        return collided_tiles, tiles

    def check_collision(self, delta_time: float, scroll: pygame.Vector2) -> None:
        self.__player.collision = {
            "top": False, "bottom": False, "right": False, "left": False
        }

        self.__player.rect.x += self.__player.velocity.x * delta_time
        for t_rect, tile in zip(*self.__get_collided_tiles(scroll)):
            tile.on_collision(self.__player)
            if not tile.is_solid:
                continue

            if self.__player.velocity.x > 0:
                self.__player.rect.right = t_rect.left
                self.__player.collision["right"] = True

            elif self.__player.velocity.x < 0:
                self.__player.rect.left = t_rect.right
                self.__player.collision["left"] = True

        self.__player.rect.y += self.__player.velocity.y * delta_time
        for t_rect, tile in zip(*self.__get_collided_tiles(scroll)):
            tile.on_collision(self.__player)
            if not tile.is_solid:
                continue

            if self.__player.velocity.y > 0:
                self.__player.rect.bottom = t_rect.top
                self.__player.collision["bottom"] = True
                self.__player.velocity.y = 0

            elif self.__player.velocity.y < 0:
                self.__player.rect.top = t_rect.bottom
                self.__player.collision["top"] = True
                self.__player.velocity.y = 0


