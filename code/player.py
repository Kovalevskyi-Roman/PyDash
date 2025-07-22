import pygame

from game_mode import GameMode, Cube, Ship, Ball, Wave


class Player:
    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, 32, 32)
        self.texture: pygame.Surface | None = None

        self.gravity: float = 2.25
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_speed: float = 8
        self.jump_high: float = -16.4

        self.collision = {
            "top": False, "bottom": False, "right": False, "left": False
        }

        self.colors = {
            pygame.Color(255, 0, 0).hex: pygame.Color("#FFE600"),
            pygame.Color(0, 255, 0).hex: pygame.Color("#3844C9"),
            pygame.Color(0, 0, 255).hex: pygame.Color("#0000FF")
        }

        self.game_modes: dict[str, GameMode] = {
            Cube.name: Cube(self),
            Ship.name: Ship(self),
            Ball.name: Ball(self),
            Wave.name: Wave(self)
        }
        self.game_mode = Cube.name

        self.is_alive = True

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        self.velocity.x = self.move_speed

        if self.game_mode != Wave.name:
            self.game_modes.get(Wave.name).first_update = True

        self.game_modes.get(self.game_mode).update(delta_time, scroll)

        if self.collision.get("right"):
            self.is_alive = False

    def draw_hit_box(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "green", [
            self.rect.x - scroll.x, self.rect.y - scroll.y,
            self.rect.width, self.rect.height
        ], 2)

    def draw(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        self.game_modes.get(self.game_mode).draw(surface, scroll)
