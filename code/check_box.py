import pygame

pygame.init()
class CheckBox:
    font = pygame.Font("../resources/fonts/regular.ttf", 14)

    def __init__(self, position: list[int], value: bool = False, text: str = "", text_col: str = "white") -> None:
        self.position = position
        self.value = value
        self.text = text
        self.text_col = text_col
        self.rendered_text = self.font.render(text, True, self.text_col)

        self.texture = pygame.image.load("../resources/textures/gui/check_box.png").convert()
        self.active_texture = pygame.image.load("../resources/textures/gui/check_box_active.png").convert_alpha()

    def get_width(self) -> int:
        return self.rendered_text.get_width() + 16 + 4

    def update(self) -> None:
        if not pygame.mouse.get_just_pressed()[0]:
            return

        if not pygame.Rect(self.position, [16, 16]).collidepoint(pygame.mouse.get_pos()):
            return

        self.value = not self.value

    def draw(self, surface: pygame.Surface) -> None:
        texture = self.texture.copy()
        if self.value:
            texture.blit(self.active_texture, [0, 0])

        surface.blit(texture, self.position)
        surface.blit(self.rendered_text, [self.position[0] + 16 + 4, self.position[1] - 1])
