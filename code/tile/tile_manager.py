import pathlib
import pygame

from .portal import CubePortal, BallPortal, ShipPortal, NormalGravityPortal, ReversedGravityPortal
from .speed_buster import SpeedBusterX1, SpeedBusterX2, SpeedBusterX3, SpeedBusterX4, SpeedBusterX5
from .blue_orb import BlueOrb
from .yellow_orb import YellowOrb
from .spike import Spike
from .tile import Tile


class TileManager:
    def __init__(self) -> None:
        self.__tile_textures: dict[str, pygame.Surface] = dict()
        self.__load_textures()

    def get_tile_textures(self) -> dict[str, pygame.Surface]:
        return self.__tile_textures.copy()

    @staticmethod
    def create_tile(name: str, position: pygame.Vector2) -> Tile | None:
        match name:
            case "block":
                return Tile(position, "block")

            case "spike":
                return Spike(position)

            case "yellow_orb":
                return YellowOrb(position)

            case "blue_orb":
                return BlueOrb(position)

            case "speed_buster_1":
                return SpeedBusterX1(position)

            case "speed_buster_2":
                return SpeedBusterX2(position)

            case "speed_buster_3":
                return SpeedBusterX3(position)

            case "speed_buster_4":
                return SpeedBusterX4(position)

            case "speed_buster_5":
                return SpeedBusterX5(position)

            case "cube_portal":
                return CubePortal(position)

            case "ball_portal":
                return BallPortal(position)

            case "ship_portal":
                return ShipPortal(position)

            case "normal_gravity_portal":
                return NormalGravityPortal(position)

            case "reversed_gravity_portal":
                return ReversedGravityPortal(position)

            case _:
                return None

    def __load_textures(self) -> None:
        path = pathlib.Path("../resources/textures/tiles/")
        for item in path.iterdir():
            if not item.is_file():
                continue

            texture = pygame.transform.scale_by(pygame.image.load(item).convert_alpha(), 2)
            self.__tile_textures.setdefault(item.name.split(".")[0], texture)

    def draw_tile_hit_box(self, surface: pygame.Surface, tile: Tile, scroll: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "red", [
            tile.position.x - scroll.x + tile.hit_box.x, tile.position.y - scroll.y + tile.hit_box.y,
            tile.hit_box.width, tile.hit_box.height
        ], 2)

    def draw_tile(self, surface: pygame.Surface, tile: Tile, scroll: pygame.Vector2) -> None:
        texture = self.__tile_textures.get(tile.texture_name, None)
        if texture is None:
            return

        texture = pygame.transform.flip(texture, tile.flipped_x, tile.flipped_y)

        surface.blit(texture, [tile.position.x - scroll.x, tile.position.y - scroll.y])
