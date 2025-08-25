import json
import pygame

from level import Level
from player import Player


class ProgressBar:
    offset = 10 * 32

    @staticmethod
    def get_level_record(level: Level) -> int:
        with open(f"../resources/data/levels/{level.level_name}.json", "r") as file:
            return json.load(file).get("record")

    @staticmethod
    def set_level_record(level: Level, record: int) -> None:
        if record > 100:
            record = 100
        elif record < 0:
            record = 0

        with open(f"../resources/data/levels/{level.level_name}.json", "r") as file:
            content: dict[str, ...] = json.load(file)

            if content.get("record") < record:
                content["record"] = record

        with open(f"../resources/data/levels/{level.level_name}.json", "w") as write_file:
            json.dump(content, write_file, indent=4)

    @staticmethod
    def get_level_finish_tile(level: Level) -> pygame.Vector2:
        finish_pos = pygame.Vector2(1, 0)
        for tile in level.tiles:
            if tile.name == "ground" or tile.name == "ceiling":
                continue
            if finish_pos.x < tile.position.x:
                finish_pos = tile.position

        return finish_pos

    @staticmethod
    def get_level_progress(level: Level, player: Player) -> float:
        return round(player.rect.x / (ProgressBar.get_level_finish_tile(level).x + ProgressBar.offset) * 100, 1)
