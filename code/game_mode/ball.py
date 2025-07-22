import pygame

from .game_mode import GameMode


class Ball(GameMode):
    name = "ball_mode"

    def __init__(self, player):
        super().__init__(player)
        self.load_texture(self.player.colors)
        self.jump_high = 0

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        self.player.rect.height = 32
        self.player.rect.width = 32
        key_press = pygame.key.get_just_pressed()
        mouse_press = pygame.mouse.get_just_pressed()

        self.player.velocity.y += self.player.gravity * delta_time
        if (self.player.collision["top"] or self.player.collision["bottom"]) and (key_press[pygame.K_SPACE] or mouse_press[0]):
            self.player.velocity.y = -self.player.gravity * 2
            self.player.gravity = -self.player.gravity
