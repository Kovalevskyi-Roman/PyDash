import pygame

from button import Button
from camera import Camera
from collider import Collider
from level import Level
from player import Player
from tile import TileManager
from .level_list_state import LevelList
from .game_state import GameState


class Play(GameState):
    name = "play"

    def __init__(self, tile_manager: TileManager, level_list: LevelList, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        self.__tile_manager = tile_manager
        self.__level_list = level_list

        self.__player = Player()
        self.__camera = Camera(self.__player, self.__window_size)
        self.__level = Level("", self.__tile_manager, self.__window_size)
        self.__collider = Collider(self.__player, self.__level, self.__window_size)

        self.load_level(self.__level_list.level_names[self.__level_list.selected_level])

        self.__paused = False
        self.__paused_surface = pygame.Surface(self.__window_size)
        self.__paused_surface.fill("#656565")

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

        key_down = pygame.key.get_just_pressed()
        if key_down[pygame.K_ESCAPE]:
            self.__paused = not self.__paused

        if self.__paused:
            if self.__resume_button.is_pressed(0):
                self.__paused = False

            if self.__back_button.is_pressed(0):
                self.__reset()
                return self.__level_list.name

            return self.name

        self.__player.update(delta_time)
        self.__camera.update_scroll()
        self.__collider.check_collision(delta_time, self.__camera.scroll)

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__level.draw(surface, self.__camera.scroll)
        self.__camera.draw(surface)

        if self.__paused:
            surface.blit(self.__paused_surface, [0, 0], special_flags=pygame.BLEND_SUB)
            self.__resume_button.draw(surface)
            self.__back_button.draw(surface)
