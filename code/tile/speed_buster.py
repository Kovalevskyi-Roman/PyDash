import pygame

from player import Player
from .tile import Tile


class SpeedBusterX1(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "speed_buster_1", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.move_speed = 9


class SpeedBusterX2(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "speed_buster_2", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.move_speed = 13.5


class SpeedBusterX3(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "speed_buster_3", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.move_speed = 17.2


class SpeedBusterX4(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "speed_buster_4", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.move_speed = 20


class SpeedBusterX5(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "speed_buster_5", *args, **kwargs)

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.move_speed = 23
