import pygame

from game_state.game_state import GameState
from game_state.level_list_state import LevelList
from level import Level
from tile import TileManager, Tile


class Editor(GameState):
    name = "editor"

    def __init__(self, level_list: LevelList, tile_manager: TileManager, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        self.__level_list = level_list
        self.__tile_manager = tile_manager

        self.__level = Level(self.__level_list.level_names[self.__level_list.selected_level],
                             self.__tile_manager, self.__window_size)

        self.__level.load()

        self.__scroll = pygame.Vector2(-10, -self.__window_size[1] / 2)
        self.__selected_tiles = set()

        self.__first_frame = True

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()

    def update(self, delta_time: float, *args, **kwargs) -> str:
        if self.__level.level_name != self.__level_list.level_names[self.__level_list.selected_level]:
            self.__level.level_name = self.__level_list.level_names[self.__level_list.selected_level]
            self.__level.load()

        if self.__first_frame:
            self.__level.level_name = self.__level_list.level_names[self.__level_list.selected_level]
            self.__level.load()
            self.__first_frame = False

        key_press = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if key_press[pygame.K_ESCAPE]:
            self.__level.save()
            self.__first_frame = True
            return "property_editor"

        if key_press[pygame.K_d]:
            self.__scroll.x += 10
        elif key_press[pygame.K_a]:
            self.__scroll.x -= 10

        if key_press[pygame.K_w]:
            self.__scroll.y -= 10
        elif key_press[pygame.K_s]:
            self.__scroll.y += 10

        if key_press[pygame.K_BACKSPACE] or key_press[pygame.K_DELETE]:
            for sel_t in self.__selected_tiles:
                self.__level.tiles.remove(sel_t)

            self.__selected_tiles.clear()

        if mouse_pressed[0] or mouse_pressed[2]:
            mouse_x = (mouse_pos[0] + self.__scroll.x) // 32 * 32
            mouse_y = (mouse_pos[1] + self.__scroll.y) // 32 * 32

            can_place = True
            for tile in self.__level.tiles:
                if tile.name == "ground" or tile.name == "ceiling":
                    continue

                if pygame.Rect(tile.position, tile.hit_box.size).collidepoint(mouse_x, mouse_y):
                    can_place = False
                    if mouse_pressed[2]:
                        self.__level.tiles.remove(tile)
                        if tile in self.__selected_tiles:
                            self.__selected_tiles.remove(tile)
                        break

                    if key_press[pygame.K_LCTRL]:
                        self.__selected_tiles.add(tile)
                        break

                    self.__selected_tiles.clear()
                    self.__selected_tiles.add(tile)

            if can_place and mouse_pressed[0]:
                self.__level.tiles.append(Tile(pygame.Vector2(mouse_x, mouse_y), "block"))
                self.__selected_tiles.clear()

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill(0)
        for tile in self.__level.tiles:
            if tile.name == "ground" or tile.name == "ceiling":
                continue

            if 0 < tile.position.x - self.__scroll.x < self.__window_size[0] and \
                    0 < tile.position.y - self.__scroll.y < self.__window_size[1]:
                self.__tile_manager.draw_tile(surface, tile, self.__scroll)
                if tile in self.__selected_tiles:
                    surf = pygame.Surface([32, 32])
                    surf.fill("green")
                    surf.set_alpha(127.5)
                    surface.blit(surf, [tile.position.x - self.__scroll.x, tile.position.y - self.__scroll.y])
        # VERTICAL LINE
        pygame.draw.line(surface, "green", [-self.__scroll.x, 0], [-self.__scroll.x, self.__window_size[1]])
        # HORIZONTAL LINE
        pygame.draw.line(surface, "#3333FF", [0, -self.__scroll.y + 32], [self.__window_size[0], -self.__scroll.y + 32])
