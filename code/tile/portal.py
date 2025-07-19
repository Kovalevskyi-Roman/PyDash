import pygame

from player import Player
from .tile import Tile


class CubePortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "cube_portal", *args, **kwargs)


class BallPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "ball_portal", *args, **kwargs)


class ShipPortal(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs):
        super().__init__(position, "ship_portal", *args, **kwargs)


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
