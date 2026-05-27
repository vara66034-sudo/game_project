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
        self.correct_object_name = "ticket"

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

    def close(self):
        self.active = False
        self.message = ""

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
            label_x = rect.x + 14
            label_y = rect.y + 18
            screen.blit(label_surface, (label_x, label_y))

        hint_surface = self.small_font.render(
            "Кликни мышкой по предмету, который похож на билет.",
            True,
            COLOR_HINT,
        )
        screen.blit(hint_surface, (box_rect.x + 30, box_rect.bottom - 40))