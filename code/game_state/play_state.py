import math

import pygame

from button import Button
from camera import Camera
from collider import Collider
from level import Level
from player import Player
from progress_bar import ProgressBar
from tile import TileManager
from .settings_state import Settings
from .level_list_state import LevelList
from .game_state import GameState


class Play(GameState):
    name = "play"

    def __init__(self, tile_manager: TileManager, level_list: LevelList, settings: Settings, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        self.__tile_manager = tile_manager
        self.__level_list = level_list
        self.__settings = settings

        self.__player = Player()
        self.__camera = Camera(self.__player, self.__window_size)
        self.__level = Level("", self.__tile_manager, self.__window_size)
        self.__collider = Collider(self.__player, self.__level, self.__window_size)

        self.load_level(self.__level_list.level_names[self.__level_list.selected_level])

        self.__paused = False
        self.__paused_surface = pygame.Surface(self.__window_size)
        self.__paused_surface.fill("#656565")

        self.__font = pygame.Font("../resources/fonts/regular.ttf", 14)

        self.__resume_button = Button(
            (self.__window_size[0] // 2 - 160, self.__window_size[1] // 2 - 40, 80, 80),
            "",
            "../resources/textures/gui/resume_button.png",
            2
        )
        self.__back_button = Button(
            (self.__window_size[0] // 2 + 80, self.__window_size[1] // 2 - 40, 80, 80),
            "",
            "../resources/textures/gui/back_button.png",
            2
        )

        self.__first_frame = True

    def __reset(self) -> None:
        self.__paused = False
        self.__player = Player()
        self.__camera = Camera(self.__player, self.__window_size)
        self.__level = Level("", self.__tile_manager, self.__window_size)
        self.__collider = Collider(self.__player, self.__level, self.__window_size)

        self.load_level(self.__level_list.level_names[self.__level_list.selected_level])

    def load_level(self, level_name: str) -> None:
        self.__level.level_name = level_name
        self.__level.load()
        self.__collider.set_level(self.__level)

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.__camera.update_window_size()
        self.__level.update_window_size()
        self.__collider.update_window_size()

        self.__paused_surface = pygame.Surface(self.__window_size)
        self.__paused_surface.fill("#656565")

        self.__resume_button.rect.topleft = (self.__window_size[0] // 2 - 160, self.__window_size[1] // 2 - 40)
        self.__back_button.rect.topleft = (self.__window_size[0] // 2 + 80, self.__window_size[1] // 2 - 40)

    def update(self, delta_time: float, *args, **kwargs) -> str:
        if self.__level.level_name != self.__level_list.level_names[self.__level_list.selected_level]:
            self.__reset()

        if self.__first_frame:
            self.__reset()
            self.__first_frame = False

        if ProgressBar.get_level_progress(self.__level, self.__player) >= 100:
            ProgressBar.set_level_record(self.__level, 100)
            return "property_editor"

        key_down = pygame.key.get_just_pressed()
        if key_down[pygame.K_ESCAPE]:
            self.__paused = not self.__paused

        if self.__paused:
            if self.__resume_button.is_pressed(0):
                self.__paused = False

            if self.__back_button.is_pressed(0):
                ProgressBar.set_level_record(
                    self.__level,
                    int(ProgressBar.get_level_progress(self.__level, self.__player))
                )
                self.__reset()
                self.__first_frame = True
                return self.__level_list.name

            return self.name

        self.__player.update(delta_time, self.__camera.scroll)
        self.__camera.update_scroll()
        self.__collider.check_collision(delta_time, self.__camera.scroll)
        self.__level.update(delta_time, self.__player)

        if not self.__player.is_alive:
            ProgressBar.set_level_record(
                self.__level,
                math.ceil(ProgressBar.get_level_progress(self.__level, self.__player))
            )
            self.__reset()
            self.__paused = not self.__settings.auto_play.value
            if self.__settings.auto_play.value:
                pygame.time.wait(100)

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__level.draw(surface, self.__camera.scroll)
        self.__camera.draw(surface)
        if self.__settings.show_player_hit_box.value:
            self.__player.draw_hit_box(surface, self.__camera.scroll)

        if self.__settings.show_hit_boxes.value:
            self.__level.draw_hit_boxes(surface, self.__camera.scroll)

        text = self.__font.render(f"{ProgressBar.get_level_progress(self.__level, self.__player)}%", True, "white", "black")
        surface.blit(text, [self.__window_size[0] / 2 - text.width / 2, 1])

        if self.__paused:
            surface.blit(self.__paused_surface, [0, 0], special_flags=pygame.BLEND_SUB)
            self.__resume_button.draw(surface)
            self.__back_button.draw(surface)
