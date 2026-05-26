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


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Project: Last Stop")

        self.clock = pygame.time.Clock()
        self.running = True

        self.level = Level()
        self.player = Player(460, 300)

        self.font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.current_message = "Осмотрись в комнате. Подойди к предмету и нажми E или пробел."

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
                self._handle_key_down(event)

            if event.type == pygame.KEYUP:
                self._handle_key_up(event)

    def _handle_key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False

        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self._interact()

        # E на английской раскладке + физическая клавиша E
        if event.key == pygame.K_e or event.scancode == 8:
            self._interact()

        # Стрелки
        if event.key == pygame.K_UP:
            self.movement["up"] = True
        if event.key == pygame.K_DOWN:
            self.movement["down"] = True
        if event.key == pygame.K_LEFT:
            self.movement["left"] = True
        if event.key == pygame.K_RIGHT:
            self.movement["right"] = True

        # WASD по физическим клавишам, работает даже на русской раскладке
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
        collision_rects = self.level.get_collision_rects()
        self.player.handle_movement(self.movement, collision_rects)

    def _interact(self):
        near_object = self.level.get_near_object(self.player.rect)

        if near_object is None:
            self.current_message = "Рядом нет ничего, с чем можно взаимодействовать."
            return

        self.current_message = near_object.message

    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        self.level.draw(self.screen)
        self.player.draw(self.screen)

        self._draw_ui()

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