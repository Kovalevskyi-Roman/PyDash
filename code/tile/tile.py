import json
import pygame

from player import Player


class Tile:
    def __init__(self, position: pygame.Vector2, name: str, *args, **kwargs) -> None:
        self.position: pygame.Vector2 = position
        self.name: str = name
        self.hit_box: pygame.Rect = pygame.Rect(0, 0, 32, 32)
        self.texture_name: str = ""

        self.flipped_x = False
        self.flipped_y = False
        self.is_solid: bool = True

        self.load()

    def load(self, name: str | None = None) -> None:
        """if name is None self.name will be used instead"""
        with open("../resources/data/tiles.json", "r") as file:
            content: list[dict[str, ...]] = json.load(file)

            if name is not None:
                self.name = name

            for tile in content:
                if tile.get("name") != self.name:
                    continue

                self.texture_name = tile.get("texture_name")
                self.is_solid = tile.get("is_solid", False)
                hit_box = tile.get("hit_box")
                self.hit_box = pygame.Rect(0, 0, 32, 32)
                if hit_box is not None:
                    self.hit_box = pygame.Rect(*hit_box)

    def to_json(self) -> dict[str, ...]:
        return {
            "name": self.name,
            "flipped": [self.flipped_x, self.flipped_y],
            "position": [self.position.x, self.position.y]
        }

    def on_collision(self, player: Player, *args, **kwargs) -> None:
        pass

    def update(self, delta_time: float, player: Player, *args, **kwargs) -> None:
        if self.name == "ground" or self.name == "ceiling":
            self.position.x = player.rect.x
