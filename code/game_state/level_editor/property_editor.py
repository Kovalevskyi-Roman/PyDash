import pygame
from pathlib import Path

from button import Button
from game_state.game_state import GameState
from game_state.level_list_state import LevelList

class PropertyEditor(GameState):
    name = "property_editor"

    def __init__(self, level_list: LevelList, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        self.__level_list = level_list

        self.__font = pygame.Font("C:/Windows/Fonts/arial.ttf", 20)
        self.__text_input_text = str(self.__level_list.level_names[self.__level_list.selected_level])
        self.__text_input_rect = pygame.Rect(0, 50, 450, 50)
        self.__text_input_rect.x = self.__window_size[0] // 2 - self.__text_input_rect.width // 2
        self.__text_input_surface = pygame.Surface(self.__text_input_rect.size)
        self.__text_input_active = False
        self.__first_frame = True

        self.__play_button = Button(
            (self.__window_size[0] // 2 - 160, self.__window_size[1] // 2 - 40, 80, 80),
            "", "../resources/textures/gui/play_button.png", 2
        )

        self.__edit_button = Button(
            (self.__window_size[0] // 2 - 40, self.__window_size[1] // 2 - 40, 80, 80),
            "", "../resources/textures/gui/edit_button.png", 2)

        self.__back_button = Button(
            (self.__window_size[0] // 2 + 80, self.__window_size[1] // 2 - 40, 80, 80),
            "", "../resources/textures/gui/back_button.png", 2
        )

    def __rename_level(self) -> None:
        path = Path(f"../resources/data/levels/{self.__level_list.level_names[self.__level_list.selected_level]}.json")
        path.rename(f"../resources/data/levels/{self.__text_input_text}.json")
        self.__level_list.level_names[self.__level_list.selected_level] = self.__text_input_text

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.__text_input_rect = pygame.Rect(0, 50, 450, 50)
        self.__text_input_rect.x = self.__window_size[0] // 2 - self.__text_input_rect.width // 2
        self.__text_input_surface = pygame.Surface(self.__text_input_rect.size)

        self.__play_button.rect.topleft = (self.__window_size[0] // 2 - 160, self.__window_size[1] // 2 - 40)
        self.__edit_button.rect.topleft = (self.__window_size[0] // 2 - 40, self.__window_size[1] // 2 - 40)
        self.__back_button.rect.topleft = (self.__window_size[0] // 2 + 80, self.__window_size[1] // 2 - 40)

    def update(self, delta_time: float, *args, **kwargs) -> str:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_just_pressed()
        key_down = pygame.key.get_just_pressed()
        if self.__first_frame:
            self.__text_input_text = str(self.__level_list.level_names[self.__level_list.selected_level])

        self.__first_frame = False

        if key_down[pygame.K_ESCAPE]:
            self.__first_frame = True
            return self.__level_list.name

        if self.__text_input_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.__text_input_active = True

        elif mouse_pressed[0] and self.__text_input_active:
            self.__rename_level()
            self.__text_input_active = False

        if self.__play_button.is_pressed(0):
            self.__first_frame = True
            return "play"

        if self.__edit_button.is_pressed(0):
            self.__first_frame = True
            return "editor"

        if self.__back_button.is_pressed(0):
            self.__first_frame = True
            return self.__level_list.name

        # TEXT INPUTTING  PS: 'DON'T PUT ANYTHING BELLOW THIS! ELSE THIS WILL NOT WORK!'
        if not self.__text_input_active:
            pygame.key.stop_text_input()
            return self.name

        pygame.key.start_text_input()
        events = pygame.event.get([pygame.TEXTINPUT, pygame.KEYDOWN])
        for event in events:
            if event.type == pygame.TEXTINPUT and len(self.__text_input_text) <= 27:
                self.__text_input_text += event.text

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.__rename_level()
                self.__text_input_active = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.__text_input_text = self.__text_input_text[:-1]

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__text_input_surface.fill("#66FF29" if self.__text_input_active else "#118807")

        rendered_text = self.__font.render(self.__text_input_text, True, 0)
        self.__text_input_surface.blit(rendered_text, [self.__text_input_rect.w // 2 - rendered_text.width // 2, 15])

        surface.blit(self.__text_input_surface, self.__text_input_rect)

        self.__play_button.draw(surface)
        self.__edit_button.draw(surface)
        self.__back_button.draw(surface)
