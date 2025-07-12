import pygame


class Button:
    def __init__(self, rect: tuple[int, int, int, int], color: str = "", texture_path: str = "", texture_scale: int = 1) -> None:
        self.rect = pygame.Rect(*rect)
        self.color = color
        self.texture_path = texture_path
        self.texture_scale = texture_scale
        self.texture: pygame.Surface | None = None

        if self.texture_path:
            self.texture = pygame.image.load(self.texture_path).convert_alpha()
            self.texture = pygame.transform.scale_by(self.texture, self.texture_scale)

    def is_hovered(self, offset_x: int = 0, offset_y: int = 0) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint([mouse_pos[0] + offset_x, mouse_pos[1] + offset_y])

    def is_pressed(self, button_id: int, offset_x: int = 0, offset_y: int = 0) -> bool:
        return self.is_hovered(offset_x, offset_y) and pygame.mouse.get_just_pressed()[button_id]

    def draw_text(self, surface: pygame.Surface, text: str, text_pos: list | tuple | None, font: pygame.Font, anti_alias: bool, f_col: str) -> None:
        rendered_text = font.render(text, anti_alias, f_col)

        if text_pos is None:
            text_pos = (
                self.rect.x + self.rect.width // 2 - rendered_text.width // 2,
                self.rect.y + self.rect.height // 2 - rendered_text.height // 2
            )

        surface.blit(rendered_text, text_pos)

    def draw(self, surface: pygame.Surface) -> None:
        if self.texture is not None:
            surface.blit(self.texture, self.rect)
            return

        pygame.draw.rect(surface, self.color, self.rect)
