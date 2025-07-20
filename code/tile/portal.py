import pygame

from player import Player
from .tile import Tile


class CubePortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "cube_portal", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.game_mode = "cube_mode"


class BallPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "ball_portal", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.game_mode = "ball_mode"


class ShipPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "ship_portal", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.game_mode = "ship_mode"


class WavePortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "wave_portal", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.game_mode = "wave_mode"


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
