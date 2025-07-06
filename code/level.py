import json
import pygame

from tile import TileManager
from tile import Tile


class Level:
    def __init__(self, level_name: str, tile_manager: TileManager, window_size: tuple[int, int]) -> None:
        self.level_name: str = level_name
        self.__tile_manager = tile_manager
        self.__window_size = window_size
        self.tiles: list[Tile] = list()

        self.load(self.level_name)

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()

    def create(self) -> None:
        for i in range(4):
            self.tiles.append(Tile(pygame.Vector2(i * 32, 32), "block"))

    def __sort_tiles(self) -> list:
        return sorted(self.tiles, key=lambda tile: tile.position.x)

    def __compress_level(self) -> list:
        self.tiles = self.__sort_tiles()
        level = list()

        if len(self.tiles) < 1:
            return level

        if len(self.tiles) == 1:
            level.append(
                {"count": 1, "tile": self.tiles[0].get_json()}
            )
            return level

        count = 1
        first_tile: dict | None = None
        for i in range(len(self.tiles) - 1):
            tile: Tile = self.tiles[i]
            next_tile: Tile = self.tiles[i + 1]

            if tile.position.x != next_tile.position.x - 32 or tile.position.y != next_tile.position.y:
                level.append(
                    {"count": count, "tile": first_tile}
                )
                count = 1
                first_tile = None
                if i == len(self.tiles) - 2:
                    first_tile = next_tile.to_json()
                continue

            count += 1
            if first_tile is None:
                first_tile = tile.to_json()

        level.append(
            {"count": count, "tile": first_tile}
        )

        return level

    def save(self, file_name: str) -> None:
        data = {
            "tiles": self.__compress_level()
        }

        with open(f"../resources/data/levels/{file_name}.json", "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def __decompress_tile(count: int, tile_data: dict) -> list[Tile]:
        tiles = list()
        x_pos = tile_data.get("position")[0]
        while count != 0:
            tile = Tile(pygame.Vector2(x_pos, tile_data.get("position")[1]), tile_data.get("name"))
            tiles.append(tile)

            x_pos += 32
            count -= 1

        return tiles

    def load(self, file_name: str) -> None:
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            for tile_group in json.load(file).get("tiles"):
                self.tiles.extend(self.__decompress_tile(tile_group.get("count"), tile_group.get("tile")))

        self.tiles = self.__sort_tiles()

    def draw(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        for tile in self.tiles:
            if 0 < tile.position.x - scroll.x < self.__window_size[0] and \
                    0 < tile.position.y - scroll.y < self.__window_size[1]:
                self.__tile_manager.draw_tile(surface, tile, scroll)
