import pygame

from player import Player
from .tile import Tile


class BlueOrb(Tile):
    def __init__(self, position: pygame.Vector2, *args, **kwargs) -> None:
        super().__init__(position, "blue_orb")
        self.__was_collided = False

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        if self.__was_collided:
            return

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.__was_collided = True
            player.gravity = -player.gravity
            player.velocity.y = player.gravity
