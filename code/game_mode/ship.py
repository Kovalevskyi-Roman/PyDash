import pygame

from .game_mode import GameMode


class Ship(GameMode):
    name = "ship_mode"

    def __init__(self, player):
        super().__init__(player)
        self.load_texture(self.player.colors)
        self.jump_high = -0.8

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        self.player.rect.height = 22
        self.player.rect.width = 32
        key_press = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()

        self.player.velocity.y += self.player.gravity * delta_time
        if key_press[pygame.K_SPACE] or mouse_press[0]:
            self.player.velocity.y += self.jump_high if self.player.gravity > 0 else -self.jump_high
