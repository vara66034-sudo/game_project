import os
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenu:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font

        self.options = [
            {"text": "Новая игра", "action": "new_game"},
            {"text": "Продолжить", "action": "continue_game"},
            {"text": "Выход", "action": "exit"},
        ]

        self.selected_index = 0
        self.message = ""

        self.game_title = "LAST STOP"

        self.background_path = "assets/player/player_menu.png"
        self.background_image = self._load_background(self.background_path)

        self.text_color = (255, 255, 255)
        self.muted_text_color = (200, 190, 220)
        self.panel_color = (0, 0, 0)
        self.panel_border = (255, 255, 255)
        self.selected_color = (55, 55, 55)

    def _load_background(self, path):
        if not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()

        target_height = 620

        image_width = image.get_width()
        image_height = image.get_height()

        scale = target_height / image_height

        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        return pygame.transform.smoothscale(image, (new_width, new_height))
    
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
        self._draw_background(screen)
        self._draw_overlay(screen)
        self._draw_decor(screen)
        self._draw_title(screen)
        self._draw_menu_panel(screen)
        self._draw_hint(screen)

    def _draw_background(self, screen):
        screen.fill((9, 7, 14))

        # Мягкая тёмная подложка
        pygame.draw.rect(screen, (14, 10, 24), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Декоративное пятно слева под героиню
        pygame.draw.circle(screen, (34, 24, 50), (300, 330), 260)
        pygame.draw.circle(screen, (22, 16, 34), (260, 350), 190)

        if self.background_image is not None:
            image_x = 105
            image_y = SCREEN_HEIGHT - self.background_image.get_height() + 8

            screen.blit(self.background_image, (image_x, image_y))

    def _draw_overlay(self, screen):
        # лёгкое затемнение всей сцены
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 65))
        screen.blit(dark_overlay, (0, 0))

        # затемнение справа под меню
        right_overlay = pygame.Surface((450, SCREEN_HEIGHT), pygame.SRCALPHA)
        right_overlay.fill((6, 5, 12, 185))
        screen.blit(right_overlay, (SCREEN_WIDTH - 450, 0))

    def _draw_decor(self, screen):
        # декоративные линии / настроение станции
        pygame.draw.line(screen, (112, 78, 146), (70, 90), (SCREEN_WIDTH - 70, 90), 2)
        pygame.draw.line(screen, (82, 56, 112), (110, 118), (SCREEN_WIDTH - 110, 118), 1)

        dots_y = 165
        for x in range(120, SCREEN_WIDTH - 120, 16):
            pygame.draw.circle(screen, (130, 94, 168), (x, dots_y), 1)

    def _draw_title(self, screen):
        title_surface = self.font.render(self.game_title, True, self.text_color)
        title_x = SCREEN_WIDTH - 350
        title_y = 95
        screen.blit(title_surface, (title_x, title_y))

        subtitle_surface = self.small_font.render(
            "story puzzle adventure",
            True,
            self.muted_text_color,
        )
        subtitle_x = title_x + 4
        subtitle_y = title_y + 44
        screen.blit(subtitle_surface, (subtitle_x, subtitle_y))

    def _draw_menu_panel(self, screen):
        panel_rect = pygame.Rect(SCREEN_WIDTH - 390, 185, 320, 260)

        pygame.draw.rect(screen, self.panel_color, panel_rect)
        pygame.draw.rect(screen, self.panel_border, panel_rect, 3)

        option_x = panel_rect.x + 24
        option_y = panel_rect.y + 28
        option_w = panel_rect.width - 48
        option_h = 46
        option_gap = 16

        for index, option in enumerate(self.options):
            rect = pygame.Rect(
                option_x,
                option_y + index * (option_h + option_gap),
                option_w,
                option_h,
            )

            if index == self.selected_index:
                pygame.draw.rect(screen, self.selected_color, rect)

            pygame.draw.rect(screen, self.panel_border, rect, 2)

            option_text = f"{index + 1}. {option['text']}"
            option_surface = self.font.render(option_text, True, self.text_color)
            screen.blit(option_surface, (rect.x + 16, rect.y + 8))

        if self.message:
            message_surface = self.small_font.render(
                self.message,
                True,
                self.muted_text_color,
            )
            message_x = panel_rect.centerx - message_surface.get_width() // 2
            message_y = panel_rect.bottom + 18
            screen.blit(message_surface, (message_x, message_y))

    def _draw_hint(self, screen):
        hint_text = "↑ ↓ — выбор     Enter — подтвердить"
        hint_surface = self.small_font.render(hint_text, True, self.muted_text_color)

        hint_x = SCREEN_WIDTH - 390
        hint_y = SCREEN_HEIGHT - 48

        screen.blit(hint_surface, (hint_x, hint_y))