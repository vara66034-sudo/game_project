import pygame

from settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_FRAME_WIDTH,
    PLAYER_FRAME_HEIGHT,
    PLAYER_RENDER_WIDTH,
    PLAYER_RENDER_HEIGHT,
    PLAYER_ANIMATION_SPEED,
)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED

        self.direction = "down"
        self.is_moving = False

        self.animation_timer = 0
        self.animation_frame_index = 1

        self.sprites = self._load_sprite_sheet("assets/player/player_sheet.png")

    def _load_sprite_sheet(self, path):
        sheet = pygame.image.load(path).convert_alpha()

        directions = ["down", "left", "right", "up"]
        sprites = {}

        for row, direction in enumerate(directions):
            sprites[direction] = []

            for col in range(3):
                frame_rect = pygame.Rect(
                    col * PLAYER_FRAME_WIDTH,
                    row * PLAYER_FRAME_HEIGHT,
                    PLAYER_FRAME_WIDTH,
                    PLAYER_FRAME_HEIGHT,
                )

                frame = pygame.Surface(
                    (PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT),
                    pygame.SRCALPHA,
                )

                frame.blit(sheet, (0, 0), frame_rect)

                frame = pygame.transform.scale(
                    frame,
                    (PLAYER_RENDER_WIDTH, PLAYER_RENDER_HEIGHT),
                )

                sprites[direction].append(frame)

        return sprites

    def handle_movement(self, movement, collision_rects):
        dx = 0
        dy = 0

        if movement["up"]:
            dy -= self.speed
            self.direction = "up"
        elif movement["down"]:
            dy += self.speed
            self.direction = "down"

        if movement["left"]:
            dx -= self.speed
            self.direction = "left"
        elif movement["right"]:
            dx += self.speed
            self.direction = "right"

        self.is_moving = dx != 0 or dy != 0

        self._move(dx, dy, collision_rects)
        self._update_animation()

    def _move(self, dx, dy, collision_rects):
        if dx != 0:
            self.rect.x += dx

            for collision_rect in collision_rects:
                if self.rect.colliderect(collision_rect):
                    if dx > 0:
                        self.rect.right = collision_rect.left
                    elif dx < 0:
                        self.rect.left = collision_rect.right

        if dy != 0:
            self.rect.y += dy

            for collision_rect in collision_rects:
                if self.rect.colliderect(collision_rect):
                    if dy > 0:
                        self.rect.bottom = collision_rect.top
                    elif dy < 0:
                        self.rect.top = collision_rect.bottom

    def _update_animation(self):
        if self.is_moving:
            self.animation_timer += PLAYER_ANIMATION_SPEED

            walk_cycle = [0, 1, 2, 1]
            cycle_index = int(self.animation_timer) % len(walk_cycle)
            self.animation_frame_index = walk_cycle[cycle_index]
        else:
            self.animation_timer = 0
            self.animation_frame_index = 1

    def draw(self, screen):
        frame = self.sprites[self.direction][self.animation_frame_index]

        draw_x = self.rect.centerx - frame.get_width() // 2
        draw_y = self.rect.bottom - frame.get_height()

        screen.blit(frame, (draw_x, draw_y))