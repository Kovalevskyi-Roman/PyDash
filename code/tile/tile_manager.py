import pathlib
import pygame

from .tile import Tile


class TileManager:
    def __init__(self) -> None:
        self.__tile_textures: dict[str, pygame.Surface] = dict()
        self.__load_textures()

        print(self.__tile_textures)

    def __load_textures(self) -> None:
        path = pathlib.Path("../resources/textures/tiles/")
        for item in path.iterdir():
            if not item.is_file():
                continue

            texture = pygame.transform.scale_by(pygame.image.load(item).convert_alpha(), 2)
            self.__tile_textures.setdefault(item.name.split(".")[0], texture)

    def draw_tile(self, surface: pygame.Surface, tile: Tile, scroll: pygame.Vector2) -> None:
        texture = self.__tile_textures.get(tile.texture_id, None)
        if texture is None:
            print(f"Tile {tile.texture_id} has no texture!")
            return

        surface.blit(texture, [tile.position.x - scroll.x, tile.position.y - scroll.y])
