import pygame

from player import Player
from .tile import Tile


class Spike(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "spike")

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        player.is_alive = False
