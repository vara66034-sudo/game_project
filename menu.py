import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_BACKGROUND,
    COLOR_DIALOGUE_BOX,
    COLOR_DIALOGUE_BORDER,
    COLOR_OPTION_SELECTED,
    COLOR_OPTION_DEFAULT,
    COLOR_TEXT,
    COLOR_HINT,
)


class MainMenu:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font

        self.options = [
            {
                "text": "Новая игра",
                "action": "new_game",
            },
            {
                "text": "Продолжить",
                "action": "continue_game",
            },
            {
                "text": "Выход",
                "action": "exit",
            },
        ]

        self.selected_index = 0
        self.message = ""

    def handle_key_down(self, event):
        if event.key == pygame.K_UP:
            self.selected_index -= 1

            if self.selected_index < 0:
                self.selected_index = len(self.options) - 1

        elif event.key == pygame.K_DOWN:
            self.selected_index += 1

            if self.selected_index >= len(self.options):
                self.selected_index = 0

        elif event.key == pygame.K_RETURN:
            return self.options[self.selected_index]["action"]

        elif pygame.K_1 <= event.key <= pygame.K_9:
            option_index = event.key - pygame.K_1

            if option_index < len(self.options):
                return self.options[option_index]["action"]

        return None

    def set_message(self, message):
        self.message = message

    def draw(self, screen):
        screen.fill(COLOR_BACKGROUND)

        panel_rect = pygame.Rect(230, 110, SCREEN_WIDTH - 460, SCREEN_HEIGHT - 220)

        pygame.draw.rect(screen, COLOR_DIALOGUE_BOX, panel_rect)
        pygame.draw.rect(screen, COLOR_DIALOGUE_BORDER, panel_rect, 3)

        title_surface = self.font.render("PROJECT: LAST STOP", True, COLOR_TEXT)
        title_x = panel_rect.centerx - title_surface.get_width() // 2
        screen.blit(title_surface, (title_x, panel_rect.y + 45))

        subtitle_surface = self.small_font.render(
            "2D top-down story puzzle adventure",
            True,
            COLOR_HINT,
        )
        subtitle_x = panel_rect.centerx - subtitle_surface.get_width() // 2
        screen.blit(subtitle_surface, (subtitle_x, panel_rect.y + 85))

        y = panel_rect.y + 150

        for index, option in enumerate(self.options):
            option_rect = pygame.Rect(panel_rect.x + 55, y, panel_rect.width - 110, 46)

            if index == self.selected_index:
                pygame.draw.rect(screen, COLOR_OPTION_SELECTED, option_rect)
            else:
                pygame.draw.rect(screen, COLOR_OPTION_DEFAULT, option_rect)

            option_text = f"{index + 1}. {option['text']}"
            option_surface = self.font.render(option_text, True, COLOR_TEXT)
            screen.blit(option_surface, (option_rect.x + 20, option_rect.y + 10))

            y += 60

        if self.message:
            message_surface = self.small_font.render(self.message, True, COLOR_HINT)
            message_x = panel_rect.centerx - message_surface.get_width() // 2
            screen.blit(message_surface, (message_x, panel_rect.bottom - 65))

        hint_surface = self.small_font.render(
            "↑ ↓ — выбор     Enter — подтвердить",
            True,
            COLOR_HINT,
        )
        hint_x = panel_rect.centerx - hint_surface.get_width() // 2
        screen.blit(hint_surface, (hint_x, panel_rect.bottom - 35))