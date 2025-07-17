import json
import pygame

from player import Player
from tile import TileManager, Tile


class Level:
    def __init__(self, level_name: str, tile_manager: TileManager, window_size: tuple[int, int]) -> None:
        self.level_name: str = level_name
        self.__tile_manager = tile_manager
        self.__window_size = window_size
        self.tiles: list[Tile] = list()

        self.load()

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()

    def __sort_tiles(self) -> list:
        sorted_tiles_dict: dict[float, list[Tile]] = dict()
        for tile in sorted(self.tiles, key=lambda t: t.position.y):
            if tile.name == "ground" or tile.name == "ceiling":
                continue

            if sorted_tiles_dict.get(tile.position.y, None) is None:
                sorted_tiles_dict.setdefault(tile.position.y, list())
                sorted_tiles_dict[tile.position.y].append(tile)
                continue

            sorted_tiles_dict[tile.position.y].append(tile)

        sorted_tiles = list()
        for val in sorted_tiles_dict.values():
            sorted_tiles.extend(sorted(val, key=lambda t: t.position.x))

        return sorted_tiles

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
                if first_tile is None:
                    level.append(
                        {"count": count, "tile": tile.to_json()}
                    )
                else:
                    level.append(
                        {"count": count, "tile": first_tile}
                    )
                count = 1
                first_tile = None
                continue

            count += 1
            if first_tile is None:
                first_tile = tile.to_json()

        if first_tile is not None:
            level.append(
                {"count": count, "tile": first_tile}
            )
        else:
            level.append(
                {"count": count, "tile": next_tile.to_json()}
            )

        return level

    def save(self, file_name: str | None = None) -> None:
        if file_name is None:
            file_name = self.level_name

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

    def load(self, file_name: str | None = None) -> None:
        if file_name is None:
            file_name = self.level_name
        try:
            with open(f"../resources/data/levels/{file_name}.json", "r") as file:
                self.tiles.clear()

                for tile_group in json.load(file).get("tiles"):
                    self.tiles.extend(self.__decompress_tile(tile_group.get("count"), tile_group.get("tile")))

                self.tiles = self.__sort_tiles()
                self.tiles.append(Tile(pygame.Vector2(0, 32), "ground"))
                self.tiles.append(Tile(pygame.Vector2(0, -1000), "ceiling"))

        except FileNotFoundError:
            self.tiles = list()

    def update(self, delta_time: float, player: Player, *args, **kwargs) -> None:
        for tile in self.tiles:
            tile.update(delta_time, player, *args, **kwargs)

    def __get_tile_by_name(self, tile_name: str) -> Tile | None:
        for tile in self.tiles:
            if tile.name == tile_name:
                return tile

        return None

    def draw_ground(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        ground_y = self.__get_tile_by_name("ground").position.y
        pygame.draw.rect(surface, "blue", [
            0, ground_y - scroll.y, self.__window_size[0], self.__window_size[1] - ground_y - scroll.y
        ])

    def draw_ceil(self, surface: pygame.Surface, scroll: pygame.Vector2):
        ceil_y = self.__get_tile_by_name("ceiling").position.y + 32
        pygame.draw.rect(surface, "red", [
            0, 0, self.__window_size[0], ceil_y - scroll.y
        ])

    def draw(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        for tile in self.tiles:
            if 0 < tile.position.x - scroll.x < self.__window_size[0] and \
                    0 < tile.position.y - scroll.y < self.__window_size[1]:
                self.__tile_manager.draw_tile(surface, tile, scroll)

        self.draw_ground(surface, scroll)
        self.draw_ceil(surface, scroll)
