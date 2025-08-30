import pygame

from .game_mode import GameMode


class Wave(GameMode):
    name = "wave_mode"

    def __init__(self, player):
        super().__init__(player)
        self.load_texture(self.player.colors)
        self.points = list()
        self.__velocity_y = self.player.velocity.y
        self.first_update = True

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        key_press = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()
        self.player.rect.width = 22
        self.player.rect.height = 22
        self.player.velocity.x = self.player.move_speed * 1.5

        if any(self.player.collision.values()):
            self.player.is_alive = False

        space_press = (key_press[pygame.K_SPACE] or mouse_press[0])
        self.player.velocity.y = -self.player.velocity.x if self.player.gravity > 0 else self.player.velocity.x
        if not space_press:
            self.player.velocity.y = -self.player.velocity.y

        if self.player.velocity.y != self.__velocity_y:
            self.points.append(self.player.rect.center)
        self.__velocity_y = self.player.velocity.y

    def __draw_lines(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        need_to_remove = []
        color = self.player.colors.get(pygame.Color(0, 255, 0).hex)
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                curr_point = self.points[i]
                next_point = self.points[i + 1]

                curr_point = [curr_point[0] - scroll.x, curr_point[1] - scroll.y]
                next_point = [next_point[0] - scroll.x, next_point[1] - scroll.y]
                if next_point[0] < 0:
                    need_to_remove.append(self.points[i])

                pygame.draw.aaline(surface, color, curr_point, next_point, 10)

            pygame.draw.aaline(
                surface,
                color,
                next_point,
                [self.player.rect.center[0] - scroll.x, self.player.rect.center[1] - scroll.y],
                10
            )
        for value in need_to_remove:
            self.points.remove(value)

    def draw(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        if self.first_update:
            self.points.append(self.player.rect.center)
            self.points.append(self.player.rect.center)
            self.first_update = False
        angle = -45
        if self.player.velocity.y > 0:
            angle = -135

        texture = pygame.transform.rotate(self.texture, angle)
        self.__draw_lines(surface, scroll)
        surface.blit(
            texture,
            [self.player.rect.x - scroll.x - 12, self.player.rect.y - scroll.y - (32 - self.player.rect.height)]
        )
