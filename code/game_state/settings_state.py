import json
import pygame

from button import Button
from select import Select
from .game_state import GameState
from check_box import CheckBox
from window import Window

class Settings(GameState):
    name = "settings"

    def __init__(self, window: Window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window = window
        self.__window_size = pygame.display.get_window_size()

        self.show_hit_boxes = CheckBox([10, 10], False, "Show tile hitboxes")
        self.show_player_hit_box = CheckBox([10, 34], False, "Show player hitbox")
        self.auto_play = CheckBox([10, 58], True, "Auto play after death")
        self.show_fps = CheckBox([10, 82], False, "Show fps")

        self.fps_select = Select(pygame.Rect(self.__window_size[0] - 110, 10, 100, 25), [30, 60, 120, 240, 1000], 1)

        self.load_settings()

    def __del__(self):
        self.save_settings()

    def save_settings(self) -> None:
        data = {
            "show_hit_boxes": self.show_hit_boxes.value,
            "show_player_hit_box": self.show_player_hit_box.value,
            "auto_play": self.auto_play.value,
            "show_fps": self.show_fps.value,
            "fps": self.fps_select.get_current_value()
        }

        with open("../resources/data/settings.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_settings(self) -> None:
        with open("../resources/data/settings.json", "r") as file:
            data: dict[str, ...] = json.load(file)

            self.show_hit_boxes.value = data.get("show_hit_boxes")
            self.show_player_hit_box.value = data.get("show_player_hit_box")
            self.auto_play.value = data.get("auto_play")
            self.show_fps.value = data.get("show_fps")
            self.fps_select.set_current_value(data.get("fps"))
            self.__window.max_fps = self.fps_select.get_current_value()

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.fps_select.rect.x = self.__window_size[0] - 110

    def update(self, delta_time: float, *args, **kwargs) -> str:
        key_press = pygame.key.get_just_pressed()

        if key_press[pygame.K_ESCAPE]:
            return "menu"

        self.show_hit_boxes.update()
        self.show_player_hit_box.update()
        self.auto_play.update()
        self.show_fps.update()
        self.fps_select.update()
        self.__window.max_fps = self.fps_select.get_current_value()

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.show_hit_boxes.draw(surface)
        self.show_player_hit_box.draw(surface)
        self.auto_play.draw(surface)
        self.show_fps.draw(surface)
        self.fps_select.draw(surface)
        fps_lbl = CheckBox.font.render("Fps:", True, "white")
        surface.blit(fps_lbl, [self.fps_select.rect.x - fps_lbl.width, self.fps_select.rect.y])
