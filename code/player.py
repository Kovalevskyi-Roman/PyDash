import pygame


class Player:
    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, 30, 30)
        self.texture: pygame.Surface | None = None

        self.gravity: float = 2.25
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_speed: float = 8
        self.jump_high: float = -16.4

        self.collision = {
            "top": False, "bottom": False, "right": False, "left": False
        }

        self.__base_color = pygame.Color("#FFE600")
        self.__second_color = pygame.Color("#3844C9")

        self.is_alive = True

        self.load_texture()

    def __set_colors(self) -> None:
        for y in range(16):
            for x in range(16):
                if self.texture.get_at([x, y]) == pygame.Color(255, 0, 0, 255):
                    self.texture.set_at([x, y], self.__base_color)

                elif self.texture.get_at([x, y]) == pygame.Color(0, 255, 0, 255):
                    self.texture.set_at([x, y], self.__second_color)

    def load_texture(self) -> None:
        self.texture = pygame.image.load("../resources/textures/player/cube_mode.png").convert_alpha()
        self.__set_colors()
        self.texture = pygame.transform.scale_by(self.texture, 2)

    def update(self, delta_time: float) -> None:
        self.velocity.x = self.move_speed
        self.velocity.y += self.gravity * delta_time

        if self.collision.get("bottom") and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.velocity.y = self.jump_high

        if self.collision.get("top") and self.gravity > 0:
            self.is_alive = False

        if self.collision.get("right"):
            self.is_alive = False

    def draw(self, surface: pygame.Surface, scroll: pygame.Vector2) -> None:
        surface.blit(self.texture, [self.rect.x - scroll.x, self.rect.y - scroll.y])
