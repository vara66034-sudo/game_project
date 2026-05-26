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


class Dialogue:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font
        self.active = False

        self.title = ""
        self.lines = []
        self.options = []
        self.selected_index = 0

    def start(self, title, lines, options):
        self.active = True
        self.title = title
        self.lines = lines
        self.options = options
        self.selected_index = 0

    def close(self):
        self.active = False
        self.title = ""
        self.lines = []
        self.options = []
        self.selected_index = 0

    def handle_key_down(self, event):
        if not self.active:
            return None

        if event.key == pygame.K_UP:
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = len(self.options) - 1

        elif event.key == pygame.K_DOWN:
            self.selected_index += 1
            if self.selected_index >= len(self.options):
                self.selected_index = 0

        elif event.key == pygame.K_RETURN:
            return self.options[self.selected_index]

        elif pygame.K_1 <= event.key <= pygame.K_9:
            option_index = event.key - pygame.K_1

            if option_index < len(self.options):
                return self.options[option_index]

        return None

    def draw(self, screen):
        if not self.active:
            return

        box_rect = pygame.Rect(80, 90, SCREEN_WIDTH - 160, SCREEN_HEIGHT - 180)

        pygame.draw.rect(screen, COLOR_DIALOGUE_BOX, box_rect)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BORDER, box_rect, 3)

        title_surface = self.font.render(self.title, True, COLOR_TEXT)
        screen.blit(title_surface, (box_rect.x + 30, box_rect.y + 25))

        y = box_rect.y + 70

        for line in self.lines:
            wrapped_lines = self._wrap_text(line, self.font, box_rect.width - 60)

            for wrapped_line in wrapped_lines:
                line_surface = self.font.render(wrapped_line, True, COLOR_TEXT)
                screen.blit(line_surface, (box_rect.x + 30, y))
                y += 30

        y += 20

        for index, option in enumerate(self.options):
            option_rect = pygame.Rect(box_rect.x + 30, y, box_rect.width - 60, 38)

            if index == self.selected_index:
                pygame.draw.rect(screen, COLOR_OPTION_SELECTED, option_rect)
            else:
                pygame.draw.rect(screen, COLOR_OPTION_DEFAULT, option_rect)

            option_text = f"{index + 1}. {option['text']}"
            option_surface = self.small_font.render(option_text, True, COLOR_TEXT)
            screen.blit(option_surface, (option_rect.x + 14, option_rect.y + 9))

            y += 46

        hint_surface = self.small_font.render(
            "1–4 — выбрать ответ     ↑ ↓ — выбор     Enter — подтвердить",
            True,
            COLOR_HINT,
        )
        screen.blit(hint_surface, (box_rect.x + 30, box_rect.bottom - 35))

    def _wrap_text(self, text, font, max_width):
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

        return lines