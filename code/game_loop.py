import pygame

from game_state import GameState, Menu, LevelList, Play
from tile import TileManager
from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window
        self.__tile_manager = TileManager()

        menu = Menu()
        level_list = LevelList(self.__tile_manager)
        play = Play(self.__tile_manager, level_list)

        self.__game_states: dict[str, GameState] = {
            Menu.name: menu,
            LevelList.name: level_list,
            Play.name: play
        }
        self.__current_game_state = Menu.name

        self.__font = pygame.Font("C:/Windows/Fonts/arial.ttf", 16)

        self.__running = True

    def __event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if event.type == pygame.WINDOWRESIZED:
                self.__window.update_size()

                for game_state in self.__game_states.values():
                    game_state.update_window_size()

    def __update(self) -> None:
        delta_time = self.__window.update_clock() * 0.01
        self.__current_game_state = self.__game_states.get(self.__current_game_state).update(delta_time)

    def __draw(self) -> None:
        self.__window.clear(pygame.Color("#232332"))
        self.__game_states.get(self.__current_game_state).draw(self.__window.surface)
        rendered_fps = self.__font.render(f"fps:{round(self.__window.clock.get_fps(), 1)}", True, "white", 0)
        self.__window.surface.blit(rendered_fps, [10, 10])
        pygame.display.update()

    def start(self) -> None:
        while self.__running:
            self.__update()
            self.__draw()
            self.__event_loop()

        pygame.quit()
