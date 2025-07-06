import json
import pygame


class Tile:
    def __init__(self, position: pygame.Vector2, name: str) -> None:
        self.position: pygame.Vector2 = position
        self.name: str = name
        self.hit_box: pygame.Rect = pygame.Rect(0, 0, 32, 32)
        self.texture_name: str = ""

        self.is_solid: bool = True
        self.has_collide_func: bool = False

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
                self.has_collide_func = tile.get("has_collide_func", False)
                hit_box = tile.get("hit_box")
                self.hit_box = pygame.Rect(0, 0, 32, 32)
                if hit_box is not None:
                    self.hit_box = pygame.Rect(*hit_box)

    def to_json(self) -> dict[str, ...]:
        return {
            "name": self.name,
            "position": [self.position.x, self.position.y]
        }

    def on_collision(self, *args, **kwargs) -> None:
        pass

    def update(self, delta_time: float, *args, **kwargs) -> None:
        ...
