import os
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Dialogue:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font

        self.active = False
        self.title = ""
        self.lines = []
        self.options = []
        self.selected_index = 0

        self.portrait_path = None
        self.portrait_image = None

        self.text_pages = []
        self.current_page_index = 0

        # OMORI-like dialogue style
        self.outer_margin = 18
        self.box_height = 235
        self.box_y = SCREEN_HEIGHT - self.box_height - 18

        self.box_bg = (0, 0, 0)
        self.box_border = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.option_selected_bg = (45, 45, 45)

        self.portrait_size = 120
        self.nameplate_height = 32

        self.text_line_height = 28
        self.option_height = 30
        self.option_gap = 6

    def start(self, title, lines, options, portrait_path=None):
        self.active = True
        self.title = title
        self.lines = lines
        self.options = options
        self.selected_index = 0

        self.portrait_path = portrait_path
        self.portrait_image = self._load_portrait(portrait_path)

        self.current_page_index = 0
        self.text_pages = self._build_text_pages()

    def close(self):
        self.active = False
        self.title = ""
        self.lines = []
        self.options = []
        self.selected_index = 0
        self.portrait_path = None
        self.portrait_image = None
        self.text_pages = []
        self.current_page_index = 0

    def _load_portrait(self, portrait_path):
        if portrait_path is None:
            return None

        if not os.path.exists(portrait_path):
            return None

        image = pygame.image.load(portrait_path).convert_alpha()

        max_w = self.portrait_size - 8
        max_h = self.portrait_size - 8

        image_w = image.get_width()
        image_h = image.get_height()

        if image_w == 0 or image_h == 0:
            return None

        scale = min(max_w / image_w, max_h / image_h)

        new_w = int(image_w * scale)
        new_h = int(image_h * scale)

        return pygame.transform.smoothscale(image, (new_w, new_h))

    def _get_layout(self):
        box_rect = pygame.Rect(
            self.outer_margin,
            self.box_y,
            SCREEN_WIDTH - self.outer_margin * 2,
            self.box_height,
        )

        portrait_area_width = 0

        if self.portrait_image is not None:
            portrait_area_width = self.portrait_size + 22

        content_x = self.outer_margin + 20 + portrait_area_width
        content_width = box_rect.right - content_x - 18

        return box_rect, content_x, content_width

    def _build_text_pages(self):
        box_rect, content_x, content_width = self._get_layout()

        wrapped_lines = []

        for line in self.lines:
            wrapped = self._wrap_text(line, self.font, content_width)
            wrapped_lines.extend(wrapped)

        if not wrapped_lines:
            return [[]]

        option_area_height = self._get_options_total_height() + 36

        text_top = self.box_y + 18
        text_bottom_without_options = box_rect.bottom - 42
        text_bottom_with_options = box_rect.bottom - option_area_height - 18

        max_lines_without_options = max(
            1,
            (text_bottom_without_options - text_top) // self.text_line_height,
        )

        max_lines_with_options = max(
            1,
            (text_bottom_with_options - text_top) // self.text_line_height,
        )

        pages = []
        index = 0
        total_lines = len(wrapped_lines)

        while index < total_lines:
            remaining_lines = total_lines - index

            # Последняя страница всегда должна оставлять место под варианты ответа
            if remaining_lines <= max_lines_with_options:
                pages.append(wrapped_lines[index:index + max_lines_with_options])
                break

            # Если весь оставшийся текст помещается без вариантов,
            # всё равно делим его так, чтобы последняя страница была короткой
            lines_before_last_page = remaining_lines - max_lines_with_options

            page_size = min(max_lines_without_options, lines_before_last_page)

            if page_size <= 0:
                page_size = 1

            pages.append(wrapped_lines[index:index + page_size])
            index += page_size

        return pages
    
    def _get_options_total_height(self):
        option_count = len(self.options)

        if option_count == 0:
            return 0

        return (
            option_count * self.option_height
            + (option_count - 1) * self.option_gap
        )

    def handle_key_down(self, event):
        if not self.active:
            return None

        is_last_page = self.current_page_index >= len(self.text_pages) - 1

        if not is_last_page:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.current_page_index += 1

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
            if self.options:
                return self.options[self.selected_index]

        elif pygame.K_1 <= event.key <= pygame.K_9:
            option_index = event.key - pygame.K_1

            if option_index < len(self.options):
                return self.options[option_index]

        return None

    def draw(self, screen):
        if not self.active:
            return

        box_rect, content_x, content_width = self._get_layout()

        pygame.draw.rect(screen, self.box_bg, box_rect)
        pygame.draw.rect(screen, self.box_border, box_rect, 3)

        self._draw_portrait(screen)
        self._draw_nameplate(screen, content_x)

        is_last_page = self.current_page_index >= len(self.text_pages) - 1

        self._draw_current_text_page(screen, content_x)

        if not is_last_page:
            self._draw_continue_hint(screen, box_rect)
            return

        self._draw_options(screen, content_x, content_width, box_rect)

    def _draw_current_text_page(self, screen, content_x):
        current_y = self.box_y + 18
        current_page = self.text_pages[self.current_page_index]

        for line in current_page:
            line_surface = self.font.render(line, True, self.text_color)
            screen.blit(line_surface, (content_x, current_y))
            current_y += self.text_line_height

    def _draw_portrait(self, screen):
        if self.portrait_image is None:
            return

        portrait_x = self.outer_margin + 16
        portrait_y = self.box_y - 92

        portrait_rect = pygame.Rect(
            portrait_x,
            portrait_y,
            self.portrait_size,
            self.portrait_size,
        )

        pygame.draw.rect(screen, self.box_bg, portrait_rect)
        pygame.draw.rect(screen, self.box_border, portrait_rect, 3)

        image_x = portrait_rect.x + (portrait_rect.w - self.portrait_image.get_width()) // 2
        image_y = portrait_rect.y + (portrait_rect.h - self.portrait_image.get_height()) // 2

        screen.blit(self.portrait_image, (image_x, image_y))

    def _draw_nameplate(self, screen, content_x):
        nameplate_width = max(90, self.small_font.size(self.title)[0] + 24)

        nameplate_rect = pygame.Rect(
            content_x,
            self.box_y - self.nameplate_height - 8,
            nameplate_width,
            self.nameplate_height,
        )

        pygame.draw.rect(screen, self.box_bg, nameplate_rect)
        pygame.draw.rect(screen, self.box_border, nameplate_rect, 3)

        title_surface = self.small_font.render(self.title, True, self.text_color)

        title_x = nameplate_rect.x + (nameplate_rect.w - title_surface.get_width()) // 2
        title_y = nameplate_rect.y + (nameplate_rect.h - title_surface.get_height()) // 2

        screen.blit(title_surface, (title_x, title_y))

    def _draw_options(self, screen, content_x, content_width, box_rect):
        if not self.options:
            return

        options_total_height = self._get_options_total_height()
        current_y = box_rect.bottom - options_total_height - 18

        for index, option in enumerate(self.options):
            option_rect = pygame.Rect(
                content_x,
                current_y,
                content_width,
                self.option_height,
            )

            if index == self.selected_index:
                pygame.draw.rect(screen, self.option_selected_bg, option_rect)

            option_text = f"{index + 1}. {option['text']}"
            option_surface = self.small_font.render(option_text, True, self.text_color)

            screen.blit(
                option_surface,
                (option_rect.x + 10, option_rect.y + 6),
            )

            current_y += self.option_height + self.option_gap

    def _draw_continue_hint(self, screen, box_rect):
        hint_text = "Enter — дальше"
        hint_surface = self.small_font.render(hint_text, True, self.text_color)

        hint_x = box_rect.right - hint_surface.get_width() - 14
        hint_y = box_rect.bottom - hint_surface.get_height() - 10

        screen.blit(hint_surface, (hint_x, hint_y))

    def _wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())

                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines