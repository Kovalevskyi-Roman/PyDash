import pygame

from .game_mode import GameMode


class Cube(GameMode):
    name = "cube_mode"

    def __init__(self, player):
        super().__init__(player)
        self.load_texture(self.player.colors)
        self.jump_high = -(self.player.gravity * self.player.gravity + self.player.gravity)

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        self.player.rect.height = 32
        self.player.rect.width = 32
        key_press = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()

        self.player.velocity.y += self.player.gravity * delta_time
        # GRAVITY > 0
        if self.player.gravity > 0:

            if self.player.collision["bottom"] and (key_press[pygame.K_SPACE] or mouse_press[0]):
                self.player.velocity.y = self.jump_high

            if self.player.collision["top"]:
                self.player.is_alive = False
            return
        # IF GRAVITY < 0
        if self.player.collision["top"] and (key_press[pygame.K_SPACE] or mouse_press[0]):
            self.player.velocity.y = -self.jump_high

        if self.player.collision["bottom"]:
            self.player.is_alive = False
