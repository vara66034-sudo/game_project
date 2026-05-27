import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_HEIGHT,
    UI_HEIGHT,
    FPS,
    DEBUG_UI,
    COLOR_BACKGROUND,
    COLOR_TEXT_BOX,
    COLOR_TEXT,
    COLOR_HINT,
)

from player import Player
from level import Level
from dialogue import Dialogue
from progress import Progress
from puzzle import FindObjectPuzzle, SequencePuzzle

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Project: Last Stop")

        self.clock = pygame.time.Clock()
        self.running = True
        self.show_debug = DEBUG_UI

        self.current_level_name = "room"
        self.progress = Progress()
        self.level = Level(self.current_level_name)

        self.player = Player(460, 300)

        self.font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.dialogue = Dialogue(self.font, self.small_font)
        self.find_ticket_puzzle = FindObjectPuzzle(self.font, self.small_font)
        self.sequence_puzzle = SequencePuzzle(self.font, self.small_font)

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

            if self.find_ticket_puzzle.active:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = self.find_ticket_puzzle.handle_mouse_down(event.pos)

                    if result is not None:
                        self._handle_ticket_puzzle_result(result)

                continue

            if self.sequence_puzzle.active:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = self.sequence_puzzle.handle_mouse_down(event.pos)

                    if result is not None:
                        self._handle_sequence_puzzle_result(result)

                continue

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

        if event.key == pygame.K_F3:
            self.show_debug = not self.show_debug

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
        if self.dialogue.active or self.find_ticket_puzzle.active or self.sequence_puzzle.active:
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

        if near_object.name == "conductor":
            self._start_conductor_dialogue()
            return
        
        if near_object.name == "school_passage":
            self._change_level("distorted_school")
            return

        if near_object.name == "symbol_door":
            self.sequence_puzzle.start()
            return

        if near_object.name == "opened_symbol_door":
            self.current_message = "Дальше будет финальная сцена, но пока она ещё не добавлена."
            return

        if near_object.name == "closed_gate":
            if self.progress.ticket_found:
                self.current_message = "Проход открыт. Можно идти дальше."
            else:
                self.current_message = "Проход закрыт. Проводник ждёт, когда ты найдёшь билет."
            return

        self.current_message = near_object.message

    def _change_level(self, level_name):
        self.current_level_name = level_name
        self.level.load_level(level_name, self.progress)

        if level_name == "room":
            self.player.rect.x = 460
            self.player.rect.y = 300
            self.current_message = "Комната. Осмотрись, затем выйди через дверь."

        elif level_name == "metro":
            self.player.rect.x = 460
            self.player.rect.y = 430
            self.current_message = "Метро. Вагон почти пустой. Найди место, чтобы сесть."

        elif level_name == "other_station":
            self.player.rect.x = 460
            self.player.rect.y = 360
            self.current_message = "Станция без названия. Здесь слишком тихо."

        elif level_name == "distorted_school":
            self.player.rect.x = 460
            self.player.rect.y = 270
            self.current_message = "Искажённая школа. Всё здесь похоже на реальность, но стоит неправильно."

        self._stop_movement()

    def _reload_current_level(self):
        self.level.load_level(self.current_level_name, self.progress)

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
                    "action": "go_other_station",
                }
            ],
        )

    def _start_conductor_dialogue(self):
        if self.progress.ticket_found:
            self.dialogue.start(
                title="Проводник",
                lines=[
                    "— Билет нашёлся.",
                    "— Значит, станция признала тебя пассажиром.",
                    "— Проход дальше открыт.",
                ],
                options=[
                    {
                        "text": "Продолжить.",
                        "connection": 0,
                        "result": "Проводник отступает в сторону. Проход больше не закрыт.",
                    }
                ],
            )
            return

        if self.progress.conductor_task_started:
            self.dialogue.start(
                title="Проводник",
                lines=[
                    "— Билет всё ещё где-то здесь.",
                    "— Иногда нужные вещи лежат среди почти одинаковых.",
                ],
                options=[
                    {
                        "text": "Искать билет.",
                        "connection": 0,
                        "result": "Героиня внимательно смотрит на разбросанные бумажки.",
                        "action": "start_ticket_puzzle",
                    },
                    {
                        "text": "Пока не сейчас.",
                        "connection": 0,
                        "result": "Проводник кивает. Станция всё равно ждёт.",
                    },
                ],
            )
            return

        self.dialogue.start(
            title="Проводник",
            lines=[
                "— Ты проехала дальше конечной.",
                "— Обычно сюда не попадают случайно.",
                "— Но если станция открылась, значит, тебе нужно что-то здесь увидеть.",
                "— Найди потерянный билет. Без него проход не откроется.",
            ],
            options=[
                {
                    "text": "Я попробую найти его.",
                    "connection": 1,
                    "result": "Проводник кивает. На полу появляются похожие бумажки.",
                    "action": "start_ticket_puzzle",
                },
                {
                    "text": "Почему именно я?",
                    "connection": 1,
                    "result": "Проводник отвечает: «Потому что ты привыкла думать, что ничего не можешь изменить».",
                    "action": "start_ticket_puzzle",
                },
                {
                    "text": "Я не хочу.",
                    "connection": 0,
                    "result": "Проводник спокойно отвечает: «Тогда станция подождёт».",
                },
            ],
        )

    def _apply_dialogue_option(self, option):
        if option.get("connection", 0) > 0:
            self.progress.add_connection_point()

        if self.current_level_name == "room":
            self.progress.mark_phone_answered()

        self.current_message = option["result"]
        self.dialogue.close()

        action = option.get("action")

        if action == "go_other_station":
            self._change_level("other_station")

        elif action == "start_ticket_puzzle":
            self.progress.start_conductor_task()
            self.find_ticket_puzzle.start()

    def _handle_ticket_puzzle_result(self, result):
        self.current_message = result["message"]

        if result["solved"]:
            self.progress.mark_ticket_found()
            self.progress.add_connection_point()
            self._reload_current_level()

    def _handle_sequence_puzzle_result(self, result):
        self.current_message = result["message"]

        if result["solved"]:
            self.progress.mark_symbol_puzzle_solved()
            self.progress.add_connection_point()
            self._reload_current_level()

    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        self.level.draw(self.screen)
        self.player.draw(self.screen)

        if self.find_ticket_puzzle.active:
            self.find_ticket_puzzle.draw(self.screen)
        elif self.sequence_puzzle.active:
            self.sequence_puzzle.draw(self.screen)
        elif self.dialogue.active:
            self.dialogue.draw(self.screen)
        else:
            self._draw_ui()

        pygame.display.flip()

    def _draw_ui(self):
        box_rect = pygame.Rect(0, GAME_HEIGHT, SCREEN_WIDTH, UI_HEIGHT)

        pygame.draw.rect(self.screen, COLOR_TEXT_BOX, box_rect)

        self._draw_wrapped_text(
            text=self.current_message,
            font=self.font,
            color=COLOR_TEXT,
            x=30,
            y=GAME_HEIGHT + 24,
            max_width=SCREEN_WIDTH - 60,
            line_height=28,
            max_lines=2,
        )

        if self.show_debug:
            debug_text = (
                f"DEBUG: level={self.current_level_name} | "
                f"connection_points={self.progress.connection_points} | "
                f"ticket_found={self.progress.ticket_found} | "
                f"symbols_solved={self.progress.symbol_puzzle_solved} | "
                f"F3 hide debug"
            )

            debug_surface = self.small_font.render(debug_text, True, COLOR_HINT)
            self.screen.blit(debug_surface, (30, GAME_HEIGHT + 78))

    def _draw_wrapped_text(self, text, font, color, x, y, max_width, line_height, max_lines=None):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        if max_lines is not None:
            lines = lines[:max_lines]

        for index, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (x, y + index * line_height))