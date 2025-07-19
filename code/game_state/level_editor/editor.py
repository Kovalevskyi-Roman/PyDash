import pygame

from game_state.game_state import GameState
from .tile_panel import TilePanel
from game_state.level_list_state import LevelList
from level import Level
from tile import TileManager


class Editor(GameState):
    name = "editor"

    def __init__(self, level_list: LevelList, tile_manager: TileManager, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__window_size = pygame.display.get_window_size()
        self.__level_list = level_list
        self.__tile_manager = tile_manager
        self.__tile_panel = TilePanel(self.__tile_manager)

        self.__level = Level(self.__level_list.level_names[self.__level_list.selected_level],
                             self.__tile_manager, self.__window_size)

        self.__level.load()

        self.__scroll = pygame.Vector2(-10, -self.__window_size[1] / 2)
        self.__selected_tiles = set()

        self.__draw_hit_boxes = False

        self.__first_frame = True

    def update_window_size(self) -> None:
        self.__window_size = pygame.display.get_window_size()
        self.__tile_panel.update_window_size()

    def __move_selected_tiles(self, x: int, y: int) -> None:
        for tile in self.__selected_tiles:
            tile.position.x += x
            tile.position.y += y

    def __flip_selected_tiles(self, x: bool, y: bool) -> None:
        for tile in self.__selected_tiles:
            tile.flipped_x = not tile.flipped_x if x else tile.flipped_x
            tile.flipped_y = not tile.flipped_y if y else tile.flipped_y

    def update(self, delta_time: float, *args, **kwargs) -> str:
        if self.__level.level_name != self.__level_list.level_names[self.__level_list.selected_level]:
            self.__level.level_name = self.__level_list.level_names[self.__level_list.selected_level]
            self.__level.load()

        if self.__first_frame:
            self.__level.level_name = self.__level_list.level_names[self.__level_list.selected_level]
            self.__level.load()
            self.__first_frame = False

        self.__tile_panel.update()

        key_press = pygame.key.get_pressed()
        key_just_press = pygame.key.get_just_pressed()
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

        if key_just_press[pygame.K_h]:
            self.__draw_hit_boxes = not self.__draw_hit_boxes

        if key_just_press[pygame.K_LEFT]:
            self.__move_selected_tiles(-2, 0)
        if key_just_press[pygame.K_RIGHT]:
            self.__move_selected_tiles(2, 0)
        if key_just_press[pygame.K_UP]:
            self.__move_selected_tiles(0, -2)
        if key_just_press[pygame.K_DOWN]:
            self.__move_selected_tiles(0, 2)

        if key_just_press[pygame.K_f]:
            self.__flip_selected_tiles(False, True)
        if key_just_press[pygame.K_g]:
            self.__flip_selected_tiles(True, False)

        if key_press[pygame.K_BACKSPACE] or key_press[pygame.K_DELETE]:
            for sel_t in self.__selected_tiles:
                self.__level.tiles.remove(sel_t)

            self.__selected_tiles.clear()

        if (mouse_pressed[0] or mouse_pressed[2]) and mouse_pos[1] < self.__tile_panel.y_pos:
            mouse_x = (mouse_pos[0] + self.__scroll.x) // 32 * 32
            mouse_y = (mouse_pos[1] + self.__scroll.y) // 32 * 32

            can_place = True
            for tile in self.__level.tiles:
                if tile.name == "ground" or tile.name == "ceiling":
                    continue

                if pygame.Rect(tile.position, tile.hit_box.size).collidepoint(mouse_pos[0] + self.__scroll.x, mouse_pos[1] + self.__scroll.y) or \
                        pygame.Rect(tile.position, [32, 32]).collidepoint(mouse_pos[0] + self.__scroll.x, mouse_pos[1] + self.__scroll.y):

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
                self.__level.tiles.append(
                    self.__tile_manager.create_tile(self.__tile_panel.selected_tile, pygame.Vector2(mouse_x, mouse_y))
                )
                self.__selected_tiles.clear()

        return self.name

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill("#222222")
        for tile in self.__level.tiles:
            if tile.name == "ground" or tile.name == "ceiling":
                continue

            if 0 < tile.position.x - self.__scroll.x < self.__window_size[0] and \
                    0 < tile.position.y - self.__scroll.y < self.__window_size[1]:
                self.__tile_manager.draw_tile(surface, tile, self.__scroll)
                if tile in self.__selected_tiles:
                    surf = pygame.Surface([32, 32])
                    if tile.hit_box.w > 32 or tile.hit_box.height > 32:
                        surf = pygame.Surface(tile.hit_box.size)
                        surf.fill("green")
                        surf.set_alpha(127.5)
                        surface.blit(surf, [tile.position.x - self.__scroll.x + tile.hit_box.x, tile.position.y - self.__scroll.y + tile.hit_box.y])
                    else:
                        surf.fill("green")
                        surf.set_alpha(127.5)
                        surface.blit(surf, [tile.position.x - self.__scroll.x, tile.position.y - self.__scroll.y])

            if self.__draw_hit_boxes:
                self.__tile_manager.draw_tile_hit_box(surface, tile, self.__scroll)
        # VERTICAL LINE
        pygame.draw.line(surface, "green", [-self.__scroll.x, 0], [-self.__scroll.x, self.__window_size[1]])
        # HORIZONTAL LINE
        pygame.draw.line(surface, "#3333FF", [0, -self.__scroll.y + 32], [self.__window_size[0], -self.__scroll.y + 32])

        self.__tile_panel.draw(surface)
