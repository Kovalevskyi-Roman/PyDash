from os import remove
import pathlib
import pygame
import random

from button import Button
from .game_state import GameState
from level import Level
from tile import TileManager


class LevelList(GameState):
    name = "level_list"

    def __init__(self, tile_manager: TileManager, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__tile_manager = tile_manager
        self.__window_size = pygame.display.get_window_size()

        self.__font = pygame.Font("C:/Windows/Fonts/arial.ttf", 20)
        self.__level_btn_width = self.__window_size[0] // 1.3
        self.__level_btn_half_width = self.__level_btn_width // 2
        self.__level_btn_height = 40
        self.__level_btn__half_height = self.__level_btn_height // 2
        self.__y_scroll = 0
        self.__x_pos = self.__window_size[0] // 2 - self.__level_btn_half_width

        self.__panel = pygame.Surface([self.__window_size[0], 80])
        self.__play_btn = Button((self.__panel.width // 2 - 200, self.__panel.height // 2 - 20, 100, 40), "#AADD29")
        self.__edit_btn = Button((self.__panel.width // 2 - 50, self.__panel.height // 2 - 20, 100, 40), "#AADD29")
        self.__delete_btn = Button((self.__panel.width // 2 + 100, self.__panel.height // 2 - 20, 100, 40), "#AADD29")

        self.level_names = []
        self.selected_level = 0
        self.__load_levels()

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.__level_btn_width = self.__window_size[0] // 1.3
        self.__level_btn_half_width = self.__level_btn_width // 2
        self.__x_pos = self.__window_size[0] // 2 - self.__level_btn_half_width

        self.__panel = pygame.Surface([self.__window_size[0], 80])
        self.__play_btn.rect.topleft = (self.__panel.width // 2 - 200, self.__panel.height // 2 - 20)
        self.__edit_btn.rect.topleft = (self.__panel.width // 2 - 50, self.__panel.height // 2 - 20)
        self.__delete_btn.rect.topleft = (self.__panel.width // 2 + 100, self.__panel.height // 2 - 20)

    def __load_levels(self) -> None:
        path = pathlib.Path("../resources/data/levels/")

        for item in path.iterdir():
            if not item.is_file():
                continue

            split_name = item.name.split(".")
            if split_name[1] != "json":
                continue

            self.level_names.append(split_name[0])

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        y = 10
        for i in range(len(self.level_names)):
            level = self.level_names[i]
            pygame.draw.rect(
                surface,
                "#118807" if self.selected_level != i else "#66FF29",
                [self.__x_pos, y + self.__y_scroll, self.__level_btn_width, self.__level_btn_height]
            )
            level_name = self.__font.render(level, True, 0)
            surface.blit(level_name, [self.__x_pos + 10, y + self.__level_btn__half_height - 10 + self.__y_scroll])
            y += 50

        pygame.draw.rect(
            surface,
            "#52CC14",
            [self.__x_pos + self.__level_btn_width - 40, y + self.__y_scroll, 40, self.__level_btn_height]
        )
        level_name = self.__font.render("+", True, 0)
        surface.blit(level_name, [self.__x_pos + self.__level_btn_width - 26,
                                  y + self.__level_btn__half_height - 10 + self.__y_scroll])

        self.__panel.fill("#52CC14")
        self.__panel.blit(self.__font.render(self.level_names[self.selected_level], True, 0),
                          [10, self.__panel.height // 2 - 10])
        self.__panel.blit(self.__font.render("Selected:", True, 0),
                          [10, self.__panel.height // 2 - 30])

        self.__play_btn.draw(self.__panel)
        self.__play_btn.draw_text(self.__panel, "Play", None, self.__font, True, 0)

        self.__edit_btn.draw(self.__panel)
        self.__edit_btn.draw_text(self.__panel, "Edit", None, self.__font, True, 0)

        self.__delete_btn.draw(self.__panel)
        self.__delete_btn.draw_text(self.__panel, "Delete", None, self.__font, True, 0)

        surface.blit(self.__panel, [0, self.__window_size[1] - self.__panel.height])

    def update(self, delta_time: float, *args, **kwargs) -> str:
        key_down = pygame.key.get_just_pressed()

        if key_down[pygame.K_ESCAPE]:
            return "menu"

        can_scroll_down: bool = len(self.level_names) * 50 + self.__y_scroll + 100 + self.__panel.height > self.__window_size[1]
        can_scroll_up: bool = self.__y_scroll < 0
        mouse_wheel = pygame.event.get(pygame.MOUSEWHEEL)
        if mouse_wheel:
            if mouse_wheel[0].y > 0 and can_scroll_up:
                self.__y_scroll += 20

            elif mouse_wheel[0].y < 0 and can_scroll_down:
                self.__y_scroll -= 20

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_just_pressed()

        y = 10
        for i in range(len(self.level_names)):
            if not mouse_pressed[0]:
                y += 50
                continue
            button = pygame.Rect(self.__x_pos, y + self.__y_scroll, self.__level_btn_width, self.__level_btn_height)
            if not button.collidepoint(mouse_pos):
                y += 50
                continue

            self.selected_level = i
            break

        if self.__play_btn.is_pressed(0, 0, -self.__window_size[1] + self.__panel.height):
            return "play"

        if self.__edit_btn.is_pressed(0, 0, -self.__window_size[1] + self.__panel.height):
            return "property_editor"

        if self.__delete_btn.is_pressed(0, 0, -self.__window_size[1] + self.__panel.height):
            remove(f"../resources/data/levels/{self.level_names[self.selected_level]}.json")
            self.level_names.pop(self.selected_level)
            self.selected_level -= 1

        button = pygame.Rect(self.__x_pos + self.__level_btn_width - 40, y + self.__y_scroll, 40,
                             self.__level_btn_height)
        if mouse_pressed[0] and button.collidepoint(mouse_pos):
            new_level = str(random.Random().randint(0, 2**16))
            self.level_names.append(new_level)
            Level(new_level, self.__tile_manager, self.__window_size).save()
            self.selected_level = len(self.level_names) - 1

        return self.name
