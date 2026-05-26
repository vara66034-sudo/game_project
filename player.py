import pygame

from settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    COLOR_PLAYER,
)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED

    def handle_movement(self, movement, collision_rects):
        dx = 0
        dy = 0

        if movement["up"]:
            dy -= self.speed
        if movement["down"]:
            dy += self.speed
        if movement["left"]:
            dx -= self.speed
        if movement["right"]:
            dx += self.speed

        self._move(dx, dy, collision_rects)

    def _move(self, dx, dy, collision_rects):
        if dx != 0:
            self.rect.x += dx
            if self._has_collision(collision_rects):
                self.rect.x -= dx

        if dy != 0:
            self.rect.y += dy
            if self._has_collision(collision_rects):
                self.rect.y -= dy

    def _has_collision(self, collision_rects):
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                return True

        return False

    def draw(self, screen):
        pygame.draw.rect(self.screen if False else screen, COLOR_PLAYER, self.rect)