import pygame


class GameMode:
    name = "game_mode"

    def __init__(self, player) -> None:
        self.player = player

        self.texture: pygame.Surface | None = None
        self.jump_high = 0

    @staticmethod
    def paint_texture(colors: dict[str, pygame.Color], texture: pygame.Surface) -> pygame.Surface:
        for y in range(texture.height):
            for x in range(texture.width):
                color = colors.get(texture.get_at([x, y]).hex, None)
                if color is None:
                    continue

                texture.set_at([x, y], color)

        return texture

    def load_texture(self, colors: dict[pygame.Color, pygame.Color]) -> None:
        self.texture = pygame.image.load(f"../resources/textures/player/{self.name}.png").convert_alpha()
        self.paint_texture(colors, self.texture)
        self.texture = pygame.transform.scale_by(self.texture, 2)

    def update(self, delta_time: float, scroll: pygame.Vector2) -> None:
        ...

    def draw(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        surface.blit(
            self.texture,
            [self.player.rect.x - scroll.x, self.player.rect.y - scroll.y - (32 - self.player.rect.height)]
        )
