import pygame

from settings import (
    CONDUCTOR_FRAME_WIDTH,
    CONDUCTOR_FRAME_HEIGHT,
    CONDUCTOR_RENDER_WIDTH,
    CONDUCTOR_RENDER_HEIGHT,
)


class StaticNPCSprite:
    def __init__(self, sprite_sheet_path, direction="down"):
        self.direction = direction
        self.sprites = self._load_sprite_sheet(sprite_sheet_path)

    def _load_sprite_sheet(self, path):
        sheet = pygame.image.load(path).convert_alpha()

        directions = ["down", "left", "right", "up"]
        sprites = {}

        for row, direction in enumerate(directions):
            sprites[direction] = []

            for col in range(3):
                frame_rect = pygame.Rect(
                    col * CONDUCTOR_FRAME_WIDTH,
                    row * CONDUCTOR_FRAME_HEIGHT,
                    CONDUCTOR_FRAME_WIDTH,
                    CONDUCTOR_FRAME_HEIGHT,
                )

                frame = pygame.Surface(
                    (CONDUCTOR_FRAME_WIDTH, CONDUCTOR_FRAME_HEIGHT),
                    pygame.SRCALPHA,
                )

                frame.blit(sheet, (0, 0), frame_rect)

                frame = pygame.transform.scale(
                    frame,
                    (CONDUCTOR_RENDER_WIDTH, CONDUCTOR_RENDER_HEIGHT),
                )

                sprites[direction].append(frame)

        return sprites

    def draw(self, screen, target_rect):
        frame = self.sprites[self.direction][1]

        draw_x = target_rect.centerx - frame.get_width() // 2
        draw_y = target_rect.bottom - frame.get_height()

        screen.blit(frame, (draw_x, draw_y))