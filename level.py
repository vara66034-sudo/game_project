import pygame

from settings import (
    SCREEN_WIDTH,
    GAME_HEIGHT,
    TILE_SIZE,
    COLOR_FLOOR,
    COLOR_WALL,
    COLOR_BED,
    COLOR_DESK,
    COLOR_MIRROR,
    COLOR_PHONE,
    COLOR_DOOR,
    COLOR_WINDOW,
)

class InteractableObject:
    def __init__(self, name, rect, color, message):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.color = color
        self.message = message

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Level:
    def __init__(self):
        self.walls = []
        self.objects = []
        self._create_room()

    def _create_room(self):
        self._create_walls()
        self._create_objects()

    def _create_walls(self):
        thickness = TILE_SIZE

        self.walls = [
            pygame.Rect(0, 0, SCREEN_WIDTH, thickness),
            pygame.Rect(0, GAME_HEIGHT - thickness, SCREEN_WIDTH, thickness),
            pygame.Rect(0, 0, thickness, GAME_HEIGHT),
            pygame.Rect(SCREEN_WIDTH - thickness, 0, thickness, GAME_HEIGHT),
        ]

    def _create_objects(self):
        bed = InteractableObject(
            name="bed",
            rect=(80, 80, 220, 90),
            color=COLOR_BED,
            message="Кровать. Кажется, сегодня сил меньше обычного.",
        )

        desk = InteractableObject(
            name="desk",
            rect=(650, 90, 180, 80),
            color=COLOR_DESK,
            message="Стол. Учебники лежат открытыми, но мысли всё равно где-то далеко.",
        )

        mirror = InteractableObject(
            name="mirror",
            rect=(90, 300, 90, 130),
            color=COLOR_MIRROR,
            message="Зеркало. Она смотрит на себя, но будто не узнаёт.",
        )

        phone = InteractableObject(
            name="phone",
            rect=(420, 390, 50, 35),
            color=COLOR_PHONE,
            message="Телефон. На экране новое сообщение.",
        )

        door = InteractableObject(
            name="door",
            rect=(850, 350, 70, 120),
            color=COLOR_DOOR,
            message="Дверь. Через неё можно выйти из комнаты, но пока сцена не готова.",
        )

        window = InteractableObject(
            name="window",
            rect=(390, 40, 180, 35),
            color=COLOR_WINDOW,
            message="Окно. Утренне солнце слепит в лицо.",
        )

        self.objects = [
            bed,
            desk,
            window,
            mirror,
            phone,
            door,
        ]

    def get_collision_rects(self):
        rects = []

        for wall in self.walls:
            rects.append(wall)

        for obj in self.objects:
            if obj.name not in ("phone", "window"):
                rects.append(obj.rect)

        return rects

    def get_near_object(self, player_rect):
        interaction_zone = player_rect.inflate(70, 70)

        for obj in self.objects:
            if interaction_zone.colliderect(obj.rect):
                return obj

        return None

    def draw(self, screen):
        room_rect = pygame.Rect(0, 0, SCREEN_WIDTH, GAME_HEIGHT)
        pygame.draw.rect(screen, COLOR_FLOOR, room_rect)

        for wall in self.walls:
            pygame.draw.rect(screen, COLOR_WALL, wall)

        for obj in self.objects:
            obj.draw(screen)