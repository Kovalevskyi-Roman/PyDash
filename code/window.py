import pygame


class Window:
    def __init__(self, size: tuple[int, int], max_fps: int) -> None:
        self.size = size
        self.max_fps = max_fps

        self.surface = pygame.display.set_mode(self.size, flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    @staticmethod
    def set_caption(text: str) -> None:
        pygame.display.set_caption(text)

    @staticmethod
    def set_icon(path: str) -> None:
        icon = pygame.image.load(path).convert_alpha()
        pygame.display.set_icon(icon)

    def update_size(self) -> None:
        self.size = pygame.display.get_window_size()
        self.surface = pygame.display.set_mode(self.size)

    def update_clock(self) -> int:
        return self.clock.tick(self.max_fps)

    def clear(self, color: pygame.Color) -> None:
        self.surface.fill(color)
