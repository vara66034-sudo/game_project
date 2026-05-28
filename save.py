import json
import os


SAVE_FILE = "save_data.json"


class SaveManager:
    def __init__(self, save_file=SAVE_FILE):
        self.save_file = save_file

    def save_game(self, level_name, player_rect, progress):
        data = {
            "level_name": level_name,
            "player": {
                "x": player_rect.x,
                "y": player_rect.y,
            },
            "progress": {
                "connection_points": progress.connection_points,
                "phone_answered": progress.phone_answered,
                "ticket_found": progress.ticket_found,
                "conductor_task_started": progress.conductor_task_started,
                "symbol_puzzle_solved": progress.symbol_puzzle_solved,
                "ending_shown": progress.ending_shown,
            },
        }

        with open(self.save_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_game(self):
        if not os.path.exists(self.save_file):
            return None

        with open(self.save_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def has_save(self):
        return os.path.exists(self.save_file)

    def delete_save(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)