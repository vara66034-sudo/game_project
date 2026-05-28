import pygame

from progress import Progress
from save import SaveManager


def test_save_and_load_game(tmp_path):
    save_file = tmp_path / "test_save.json"

    save_manager = SaveManager(save_file=str(save_file))

    progress = Progress()
    progress.add_connection_point()
    progress.mark_phone_answered()
    progress.start_conductor_task()
    progress.mark_ticket_found()
    progress.mark_symbol_puzzle_solved()

    player_rect = pygame.Rect(100, 150, 28, 28)

    save_manager.save_game(
        level_name="distorted_school",
        player_rect=player_rect,
        progress=progress,
    )

    loaded_data = save_manager.load_game()

    assert loaded_data is not None
    assert loaded_data["level_name"] == "distorted_school"
    assert loaded_data["player"]["x"] == 100
    assert loaded_data["player"]["y"] == 150
    assert loaded_data["progress"]["connection_points"] == 1
    assert loaded_data["progress"]["phone_answered"] is True
    assert loaded_data["progress"]["conductor_task_started"] is True
    assert loaded_data["progress"]["ticket_found"] is True
    assert loaded_data["progress"]["symbol_puzzle_solved"] is True


def test_has_save_returns_false_if_file_does_not_exist(tmp_path):
    save_file = tmp_path / "missing_save.json"

    save_manager = SaveManager(save_file=str(save_file))

    assert save_manager.has_save() is False


def test_delete_save(tmp_path):
    save_file = tmp_path / "test_save.json"

    save_manager = SaveManager(save_file=str(save_file))

    progress = Progress()
    player_rect = pygame.Rect(0, 0, 28, 28)

    save_manager.save_game(
        level_name="room",
        player_rect=player_rect,
        progress=progress,
    )

    assert save_manager.has_save() is True

    save_manager.delete_save()

    assert save_manager.has_save() is False