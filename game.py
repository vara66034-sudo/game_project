import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_HEIGHT,
    UI_HEIGHT,
    FPS,
    COLOR_BACKGROUND,
    COLOR_TEXT_BOX,
    COLOR_TEXT,
    COLOR_HINT,
)

from player import Player
from level import Level
from dialogue import Dialogue
from progress import Progress


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Project: Last Stop")

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_level_name = "room"
        self.level = Level(self.current_level_name)

        self.player = Player(460, 300)
        self.progress = Progress()

        self.font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.dialogue = Dialogue(self.font, self.small_font)

        self.current_message = "Комната. Осмотрись, затем выйди через дверь."

        self.movement = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            self._handle_events()
            self._update()
            self._draw()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.dialogue.active:
                    selected_option = self.dialogue.handle_key_down(event)

                    if selected_option is not None:
                        self._apply_dialogue_option(selected_option)

                    continue

                self._handle_key_down(event)

            if event.type == pygame.KEYUP:
                self._handle_key_up(event)

    def _handle_key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False

        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self._interact()

        if event.key == pygame.K_e or event.scancode == 8:
            self._interact()

        if event.key == pygame.K_UP:
            self.movement["up"] = True
        if event.key == pygame.K_DOWN:
            self.movement["down"] = True
        if event.key == pygame.K_LEFT:
            self.movement["left"] = True
        if event.key == pygame.K_RIGHT:
            self.movement["right"] = True

        if event.scancode == 26:  # W
            self.movement["up"] = True
        if event.scancode == 22:  # S
            self.movement["down"] = True
        if event.scancode == 4:  # A
            self.movement["left"] = True
        if event.scancode == 7:  # D
            self.movement["right"] = True

    def _handle_key_up(self, event):
        if event.key == pygame.K_UP:
            self.movement["up"] = False
        if event.key == pygame.K_DOWN:
            self.movement["down"] = False
        if event.key == pygame.K_LEFT:
            self.movement["left"] = False
        if event.key == pygame.K_RIGHT:
            self.movement["right"] = False

        if event.scancode == 26:  # W
            self.movement["up"] = False
        if event.scancode == 22:  # S
            self.movement["down"] = False
        if event.scancode == 4:  # A
            self.movement["left"] = False
        if event.scancode == 7:  # D
            self.movement["right"] = False

    def _update(self):
        if self.dialogue.active:
            return

        collision_rects = self.level.get_collision_rects()
        self.player.handle_movement(self.movement, collision_rects)

    def _interact(self):
        near_object = self.level.get_near_object(self.player.rect)

        if near_object is None:
            self.current_message = "Рядом нет ничего, с чем можно взаимодействовать."
            return

        if near_object.name == "phone":
            self._start_phone_dialogue()
            return

        if near_object.name == "room_exit":
            self._change_level("metro")
            return

        if near_object.name == "metro_seat":
            self._start_metro_sleep_dialogue()
            return

        self.current_message = near_object.message

    def _change_level(self, level_name):
        self.current_level_name = level_name
        self.level.load_level(level_name)

        if level_name == "room":
            self.player.rect.x = 460
            self.player.rect.y = 300
            self.current_message = "Комната. Осмотрись, затем выйди через дверь."

        elif level_name == "metro":
            self.player.rect.x = 460
            self.player.rect.y = 430
            self.current_message = "Метро. Вагон почти пустой. Найди место, чтобы сесть."

        self._stop_movement()

    def _stop_movement(self):
        self.movement = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

    def _start_phone_dialogue(self):
        if self.progress.phone_answered:
            self.current_message = "Телефон. Сообщение уже прочитано."
            return

        self.dialogue.start(
            title="Телефон",
            lines=[
                "На экране сообщение от одноклассницы:",
                "«Ты сегодня быстро ушла. Всё нормально?»",
            ],
            options=[
                {
                    "text": "Да, всё нормально.",
                    "connection": 0,
                    "result": "Она быстро печатает ответ и убирает телефон.",
                },
                {
                    "text": "Не знаю.",
                    "connection": 1,
                    "result": "Она отвечает честнее, чем собиралась. Это маленький, но важный шаг.",
                },
                {
                    "text": "Просто устала.",
                    "connection": 1,
                    "result": "Она не пишет всего, что чувствует, но хотя бы не прячет это полностью.",
                },
                {
                    "text": "Не отвечать.",
                    "connection": 0,
                    "result": "Экран гаснет. В комнате снова становится тихо.",
                },
            ],
        )

    def _start_metro_sleep_dialogue(self):
        self.dialogue.start(
            title="Метро",
            lines=[
                "Героиня садится у окна.",
                "Станции сменяются одна за другой, но в вагоне становится всё тише.",
                "Она закрывает глаза всего на минуту.",
            ],
            options=[
                {
                    "text": "Продолжить.",
                    "connection": 0,
                    "result": "Поезд проезжает конечную станцию. Двери не открываются.",
                }
            ],
        )

    def _apply_dialogue_option(self, option):
        if option["connection"] > 0:
            self.progress.add_connection_point()

        if self.current_level_name == "room":
            self.progress.mark_phone_answered()

        self.current_message = option["result"]
        self.dialogue.close()

    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        self.level.draw(self.screen)
        self.player.draw(self.screen)

        self._draw_ui()
        self.dialogue.draw(self.screen)

        pygame.display.flip()

    def _draw_ui(self):
        box_rect = pygame.Rect(0, GAME_HEIGHT, SCREEN_WIDTH, UI_HEIGHT)

        pygame.draw.rect(self.screen, COLOR_TEXT_BOX, box_rect)

        message_surface = self.font.render(self.current_message, True, COLOR_TEXT)
        self.screen.blit(message_surface, (30, GAME_HEIGHT + 25))

        hint_surface = self.small_font.render(
            "WASD / стрелки — движение     E / пробел — взаимодействие     Esc — выход",
            True,
            COLOR_HINT,
        )
        self.screen.blit(hint_surface, (30, GAME_HEIGHT + 75))

        points_surface = self.small_font.render(
            f"connection_points: {self.progress.connection_points}",
            True,
            COLOR_HINT,
        )
        self.screen.blit(points_surface, (SCREEN_WIDTH - 220, GAME_HEIGHT + 75))