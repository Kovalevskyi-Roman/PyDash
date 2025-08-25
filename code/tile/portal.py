import pygame

from player import Player
from .tile import Tile


class CubePortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "cube_portal", *args, **kwargs)

    def on_collision(self, player: Player, level, *args, **kwargs) -> None:
        player.game_mode = "cube_mode"
        level.get_tile_by_name("ground").position.y = 32
        level.get_tile_by_name("ceiling").position.y = -1000


class BallPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "ball_portal", *args, **kwargs)
        self.__space = 5

    def on_collision(self, player: Player, level, *args, **kwargs) -> None:
        player.game_mode = "ball_mode"
        level.get_tile_by_name("ceiling").position.y = self.position.y - self.__space * 32

        level.get_tile_by_name("ground").position.y = self.__space * 32 + self.position.y + self.hit_box.height
        if level.get_tile_by_name("ground").position.y > 32:
            level.get_tile_by_name("ceiling").position.y -= level.get_tile_by_name("ground").position.y // 32 * 32
            level.get_tile_by_name("ground").position.y = 32


class ShipPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "ship_portal", *args, **kwargs)
        self.__space = 6

    def on_collision(self, player: Player, level, *args, **kwargs) -> None:
        player.game_mode = "ship_mode"
        level.get_tile_by_name("ceiling").position.y = self.position.y - self.__space * 32

        level.get_tile_by_name("ground").position.y = self.__space * 32 + self.position.y + self.hit_box.height
        if level.get_tile_by_name("ground").position.y > 32:
            level.get_tile_by_name("ceiling").position.y -= level.get_tile_by_name("ground").position.y // 32 * 32
            level.get_tile_by_name("ground").position.y = 32


class WavePortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "wave_portal", *args, **kwargs)
        self.__space = 5

    def on_collision(self, player: Player, level, *args, **kwargs) -> None:
        player.game_mode = "wave_mode"
        level.get_tile_by_name("ceiling").position.y = self.position.y - self.__space * 32

        level.get_tile_by_name("ground").position.y = self.__space * 32 + self.position.y + self.hit_box.height
        if level.get_tile_by_name("ground").position.y > 32:
            level.get_tile_by_name("ceiling").position.y -= level.get_tile_by_name("ground").position.y // 32 * 32
            level.get_tile_by_name("ground").position.y = 32


class NormalGravityPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "normal_gravity_portal", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.gravity = abs(player.gravity)


class ReversedGravityPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "reversed_gravity_portal", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.gravity = -abs(player.gravity)
