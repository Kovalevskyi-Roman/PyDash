import pygame

pygame.init()
class Select:
    font = pygame.Font("../resources/fonts/regular.ttf", 14)

    def __init__(self, rect: pygame.Rect, values: tuple | list, default: int = 0) -> None:
        self.rect = rect
        self.values = values
        self.selected = default

        self.active = False

    def get_current_value(self):
        return self.values[self.selected]

    def set_current_value(self, value) -> None:
        for i in range(len(self.values)):
            if self.values[i] == value:
                self.selected = i
                break

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_just_pressed()

        if self.rect.collidepoint(mouse_pos) and mouse_press[0]:
            self.active = not self.active

        if not self.active:
            return

        rect = pygame.Rect(self.rect.bottomleft, self.rect.size)
        for i in range(len(self.values)):
            if rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.selected = i
                self.active = False
                break
            rect.y += self.rect.height

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "#595959", self.rect)
        value = self.font.render(str(self.values[self.selected]), True, "white")
        surface.blit(value, [self.rect.x + self.rect.w // 2 - value.width // 2,
                             self.rect.y + self.rect.h // 2 - value.height // 2])

        if not self.active:
            return

        rect = pygame.Rect(self.rect.bottomleft, self.rect.size)
        for val in self.values:
            pygame.draw.rect(surface, "#595959", rect)
            value = self.font.render(str(val), True, "white")
            surface.blit(value, [rect.x + rect.w // 2 - value.width // 2,
                                 rect.y + rect.h // 2 - value.height // 2])
            rect.y += self.rect.height
