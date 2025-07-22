import pygame

from .game_mode import GameMode


class Wave(GameMode):
    name = "wave_mode"

    def __init__(self, player):
        super().__init__(player)
        self.load_texture(self.player.colors)
        self.points = list()
        self.__space_press = False
        self.__gravity = self.player.gravity
        self.first_update = True

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        key_press = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()
        self.player.rect.width = 24
        self.player.rect.height = 24

        if any(self.player.collision.values()):
            self.player.is_alive = False

        space_press = (key_press[pygame.K_SPACE] or mouse_press[0])
        if space_press != self.__space_press or self.__gravity != self.player.gravity:
            self.points.append(self.player.rect.center)
        self.__space_press = space_press
        self.__gravity = self.player.gravity

        if space_press:
            self.player.velocity.y = -self.player.move_speed if self.player.gravity > 0 else self.player.move_speed

        else:
            self.player.velocity.y = self.player.move_speed if self.player.gravity > 0 else -self.player.move_speed

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

                pygame.draw.line(surface, color, curr_point, next_point, 10)

            pygame.draw.line(surface, color, next_point,
                             [self.player.rect.center[0] - scroll.x, self.player.rect.center[1] - scroll.y], 10)
            return
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
