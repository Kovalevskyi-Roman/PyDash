import pygame


class Player:
    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, 30, 30)
        self.texture: pygame.Surface | None = None

        self.velocity = pygame.Vector2(0, 0)
        self.move_speed = 4
        self.jump_high = -5

        self.collision = {
            "top": False, "bottom": False, "right": False, "left": False
        }

        self.__base_color = pygame.Color("#FFE600")
        self.__second_color = pygame.Color("#3844C9")

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

        if not self.collision.get("bottom"):
            self.velocity.y += 0.1

        self.rect.x += self.velocity.x * delta_time
        self.rect.y += self.velocity.y * delta_time

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, [self.rect.x, self.rect.y])
