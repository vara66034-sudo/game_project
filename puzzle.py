import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_DIALOGUE_BOX,
    COLOR_DIALOGUE_BORDER,
    COLOR_OPTION_SELECTED,
    COLOR_OPTION_DEFAULT,
    COLOR_TEXT,
    COLOR_HINT,
)


class FindObjectPuzzle:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font
        self.active = False
        self.solved = False
        self.message = ""
        self.objects = []

    def start(self):
        self.active = True
        self.solved = False
        self.message = "Найди настоящий билет."

        self.objects = [
            {
                "name": "paper_1",
                "rect": pygame.Rect(170, 220, 120, 55),
                "label": "чек",
                "correct": False,
            },
            {
                "name": "paper_2",
                "rect": pygame.Rect(420, 200, 120, 55),
                "label": "листок",
                "correct": False,
            },
            {
                "name": "ticket",
                "rect": pygame.Rect(650, 260, 120, 55),
                "label": "билет",
                "correct": True,
            },
            {
                "name": "paper_3",
                "rect": pygame.Rect(300, 370, 120, 55),
                "label": "записка",
                "correct": False,
            },
            {
                "name": "paper_4",
                "rect": pygame.Rect(560, 390, 120, 55),
                "label": "обрывок",
                "correct": False,
            },
        ]

    def handle_mouse_down(self, mouse_pos):
        if not self.active:
            return None

        for item in self.objects:
            if item["rect"].collidepoint(mouse_pos):
                if item["correct"]:
                    self.solved = True
                    self.active = False
                    return {
                        "solved": True,
                        "message": "Ты нашла потерянный билет. На нём написано твоё имя.",
                    }

                self.message = "Это не билет. Просто чужая бумажка."
                return {
                    "solved": False,
                    "message": self.message,
                }

        return None

    def draw(self, screen):
        if not self.active:
            return

        overlay_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BOX, overlay_rect)

        box_rect = pygame.Rect(80, 70, SCREEN_WIDTH - 160, SCREEN_HEIGHT - 140)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BOX, box_rect)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BORDER, box_rect, 3)

        title_surface = self.font.render("Мини-игра: потерянный билет", True, COLOR_TEXT)
        screen.blit(title_surface, (box_rect.x + 30, box_rect.y + 25))

        message_surface = self.small_font.render(self.message, True, COLOR_HINT)
        screen.blit(message_surface, (box_rect.x + 30, box_rect.y + 65))

        for item in self.objects:
            rect = item["rect"]

            pygame.draw.rect(screen, COLOR_OPTION_DEFAULT, rect)
            pygame.draw.rect(screen, COLOR_DIALOGUE_BORDER, rect, 2)

            label_surface = self.small_font.render(item["label"], True, COLOR_TEXT)
            screen.blit(label_surface, (rect.x + 14, rect.y + 18))

        hint_surface = self.small_font.render(
            "Кликни мышкой по предмету, который похож на билет.",
            True,
            COLOR_HINT,
        )
        screen.blit(hint_surface, (box_rect.x + 30, box_rect.bottom - 40))


class SequencePuzzle:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font
        self.active = False
        self.solved = False

        self.correct_sequence = ["square", "circle", "triangle"]
        self.player_sequence = []
        self.message = ""

        self.symbols = []

    def start(self):
        self.active = True
        self.solved = False
        self.player_sequence = []
        self.message = "Нажми символы в правильном порядке: квадрат, круг, треугольник."

        self.symbols = [
            {
                "name": "circle",
                "label": "круг",
                "rect": pygame.Rect(210, 270, 150, 70),
            },
            {
                "name": "triangle",
                "label": "треугольник",
                "rect": pygame.Rect(405, 270, 150, 70),
            },
            {
                "name": "square",
                "label": "квадрат",
                "rect": pygame.Rect(600, 270, 150, 70),
            },
        ]

    def handle_mouse_down(self, mouse_pos):
        if not self.active:
            return None

        for symbol in self.symbols:
            if symbol["rect"].collidepoint(mouse_pos):
                self.player_sequence.append(symbol["name"])
                return self._check_sequence()

        return None

    def _check_sequence(self):
        current_index = len(self.player_sequence) - 1

        if self.player_sequence[current_index] != self.correct_sequence[current_index]:
            self.player_sequence = []
            self.message = "Неверный порядок. Символы будто возвращаются на место."
            return {
                "solved": False,
                "message": self.message,
            }

        if self.player_sequence == self.correct_sequence:
            self.solved = True
            self.active = False
            return {
                "solved": True,
                "message": "Символы вспыхнули в правильном порядке. Дверь открылась.",
            }

        self.message = "Символ принят. Продолжай."
        return {
            "solved": False,
            "message": self.message,
        }

    def draw(self, screen):
        if not self.active:
            return

        overlay_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BOX, overlay_rect)

        box_rect = pygame.Rect(80, 70, SCREEN_WIDTH - 160, SCREEN_HEIGHT - 140)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BOX, box_rect)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BORDER, box_rect, 3)

        title_surface = self.font.render("Головоломка: дверь с символами", True, COLOR_TEXT)
        screen.blit(title_surface, (box_rect.x + 30, box_rect.y + 25))

        message_surface = self.small_font.render(self.message, True, COLOR_HINT)
        screen.blit(message_surface, (box_rect.x + 30, box_rect.y + 70))

        sequence_text = "Введено: " + " → ".join(self.player_sequence)
        sequence_surface = self.small_font.render(sequence_text, True, COLOR_HINT)
        screen.blit(sequence_surface, (box_rect.x + 30, box_rect.y + 105))

        for symbol in self.symbols:
            rect = symbol["rect"]

            pygame.draw.rect(screen, COLOR_OPTION_DEFAULT, rect)
            pygame.draw.rect(screen, COLOR_DIALOGUE_BORDER, rect, 2)

            label_surface = self.font.render(symbol["label"], True, COLOR_TEXT)
            label_x = rect.x + 22
            label_y = rect.y + 20
            screen.blit(label_surface, (label_x, label_y))

        hint_surface = self.small_font.render(
            "Кликни по символам мышкой.",
            True,
            COLOR_HINT,
        )
        screen.blit(hint_surface, (box_rect.x + 30, box_rect.bottom - 40))