import os
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
    COLOR_METRO_FLOOR,
    COLOR_METRO_WALL,
    COLOR_METRO_SEAT,
    COLOR_METRO_DOOR,
    COLOR_METRO_SCREEN,
    COLOR_METRO_RAIL,
    COLOR_OTHER_FLOOR,
    COLOR_OTHER_WALL,
    COLOR_OTHER_PLATFORM,
    COLOR_OTHER_DOOR,
    COLOR_OTHER_SIGN,
    COLOR_CONDUCTOR,
    COLOR_STRANGE_LIGHT,
    COLOR_SCHOOL_FLOOR,
    COLOR_SCHOOL_WALL,
    COLOR_SCHOOL_DESK,
    COLOR_SCHOOL_BOARD,
    COLOR_SCHOOL_DOOR,
    COLOR_SYMBOL_PANEL,
    COLOR_FINAL_FLOOR,
    COLOR_FINAL_WALL,
    COLOR_FINAL_PLATFORM,
    COLOR_FINAL_SIGN,
    COLOR_FINAL_GATE,
)


class InteractableObject:
    def __init__(self, name, rect, color, message, blocks_movement=True):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.color = color
        self.message = message
        self.blocks_movement = blocks_movement

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Level:
    def __init__(self, level_name):
        self.level_name = level_name
        self.floor_color = COLOR_FLOOR
        self.wall_color = COLOR_WALL
        self.walls = []
        self.objects = []
        self.background_image = None

        self.load_level(level_name)

    def load_level(self, level_name, progress=None):
        self.level_name = level_name
        self.walls = []
        self.objects = []
        self.background_image = None

        if level_name == "room":
            self._create_room()
        elif level_name == "metro":
            self._create_metro()
        elif level_name == "other_station":
            self._create_other_station(progress)
        elif level_name == "distorted_school":
            self._create_distorted_school(progress)
        elif level_name == "final_station":
            self._create_final_station()
            
    def _create_base_walls(self, wall_color):
        thickness = TILE_SIZE

        self.walls = [
            pygame.Rect(0, 0, SCREEN_WIDTH, thickness),
            pygame.Rect(0, GAME_HEIGHT - thickness, SCREEN_WIDTH, thickness),
            pygame.Rect(0, 0, thickness, GAME_HEIGHT),
            pygame.Rect(SCREEN_WIDTH - thickness, 0, thickness, GAME_HEIGHT),
        ]

        self.wall_color = wall_color

    def _load_background(self, path):
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            self.background_image = pygame.transform.scale(
                image,
                (SCREEN_WIDTH, GAME_HEIGHT),
            )
        else:
            self.background_image = None

    def _create_room(self):
        self.floor_color = COLOR_FLOOR
        self._create_base_walls(COLOR_WALL)
        self._load_background("assets/locations/room.png")

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

        window = InteractableObject(
            name="window",
            rect=(390, 40, 180, 35),
            color=COLOR_WINDOW,
            message="Окно. За ним вечерний город, но сегодня он кажется особенно далёким.",
            blocks_movement=False,
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
            blocks_movement=False,
        )

        door = InteractableObject(
            name="room_exit",
            rect=(850, 350, 70, 120),
            color=COLOR_DOOR,
            message="Дверь. Пора выйти из комнаты.",
        )

        self.objects = [
            bed,
            desk,
            window,
            mirror,
            phone,
            door,
        ]

    def _create_metro(self):
        self.floor_color = COLOR_METRO_FLOOR
        self._create_base_walls(COLOR_METRO_WALL)
        self._load_background("assets/locations/metro.png")

        left_window = InteractableObject(
            name="metro_window",
            rect=(90, 80, 210, 55),
            color=COLOR_METRO_DOOR,
            message="За окном темнота тоннеля. В отражении почти не видно лица.",
            blocks_movement=False,
        )

        center_window = InteractableObject(
            name="metro_window",
            rect=(375, 80, 210, 55),
            color=COLOR_METRO_DOOR,
            message="Стекло дрожит от движения поезда.",
            blocks_movement=False,
        )

        right_window = InteractableObject(
            name="metro_window",
            rect=(660, 80, 210, 55),
            color=COLOR_METRO_DOOR,
            message="За окном мелькают редкие огни.",
            blocks_movement=False,
        )

        metro_screen = InteractableObject(
            name="metro_screen",
            rect=(360, 155, 240, 45),
            color=COLOR_METRO_SCREEN,
            message="Табло мигает: «Следующая станция — конечная».",
            blocks_movement=False,
        )

        left_train_door = InteractableObject(
            name="train_door",
            rect=(45, 220, 70, 140),
            color=COLOR_METRO_DOOR,
            message="Двери закрыты. За ними только тёмный тоннель.",
        )

        right_train_door = InteractableObject(
            name="train_door",
            rect=(845, 220, 70, 140),
            color=COLOR_METRO_DOOR,
            message="Двери не открываются, хотя поезд уже должен был остановиться.",
        )

        left_seat = InteractableObject(
            name="metro_seat",
            rect=(140, 390, 260, 70),
            color=COLOR_METRO_SEAT,
            message="Сиденье. Вагон почти пустой. Глаза начинают закрываться.",
        )

        right_seat = InteractableObject(
            name="metro_seat",
            rect=(560, 390, 260, 70),
            color=COLOR_METRO_SEAT,
            message="Сиденье. Здесь тихо, будто поезд едет не по обычному маршруту.",
        )

        left_rail = InteractableObject(
            name="rail",
            rect=(430, 250, 14, 110),
            color=COLOR_METRO_RAIL,
            message="Поручень холодный на ощупь.",
        )

        right_rail = InteractableObject(
            name="rail",
            rect=(515, 250, 14, 110),
            color=COLOR_METRO_RAIL,
            message="Поручень холодный на ощупь.",
        )

        self.objects = [
            left_window,
            center_window,
            right_window,
            metro_screen,
            left_train_door,
            right_train_door,
            left_seat,
            right_seat,
            left_rail,
            right_rail,
        ]

    def _create_other_station(self, progress=None):
        self.floor_color = COLOR_OTHER_FLOOR
        self._create_base_walls(COLOR_OTHER_WALL)
        self._load_background("assets/locations/other_station.png")

        platform = InteractableObject(
            name="platform",
            rect=(90, 330, 780, 90),
            color=COLOR_OTHER_PLATFORM,
            message="Платформа похожа на обычную станцию, но линии на полу слегка двигаются.",
            blocks_movement=False,
        )

        sign = InteractableObject(
            name="station_sign",
            rect=(320, 80, 320, 55),
            color=COLOR_OTHER_SIGN,
            message="Табличка станции. Буквы складываются в слова: «Станция без названия».",
            blocks_movement=False,
        )

        strange_light_left = InteractableObject(
            name="strange_light",
            rect=(130, 120, 70, 70),
            color=COLOR_STRANGE_LIGHT,
            message="Светильник тихо гудит, будто пытается что-то сказать.",
            blocks_movement=True,
        )

        strange_light_right = InteractableObject(
            name="strange_light",
            rect=(760, 120, 70, 70),
            color=COLOR_STRANGE_LIGHT,
            message="Свет дрожит, хотя воздуха здесь почти нет.",
            blocks_movement=True,
        )

        closed_gate = InteractableObject(
            name="closed_gate",
            rect=(410, 430, 140, 60),
            color=COLOR_OTHER_DOOR,
            message="Проход закрыт. Кажется, кто-то должен разрешить идти дальше.",
            blocks_movement=True,
        )

        conductor = InteractableObject(
            name="conductor",
            rect=(460, 230, 42, 58),
            color=COLOR_CONDUCTOR,
            message="Проводник молча смотрит на героиню.",
            blocks_movement=True,
        )

        self.objects = [
            platform,
            sign,
            strange_light_left,
            strange_light_right,
            conductor,
        ]

        if progress is None or not progress.ticket_found:
            self.objects.append(closed_gate)
        else:
            passage = InteractableObject(
                name="school_passage",
                rect=(410, 430, 140, 60),
                color=COLOR_OTHER_DOOR,
                message="Проход открыт. За ним виден школьный коридор, которого здесь быть не должно.",
                blocks_movement=True,
            )
            self.objects.append(passage)

    def _create_distorted_school(self, progress=None):
        self.floor_color = COLOR_SCHOOL_FLOOR
        self._create_base_walls(COLOR_SCHOOL_WALL)
        self._load_background("assets/locations/distorted_school.png")

        board = InteractableObject(
            name="school_board",
            rect=(310, 70, 340, 70),
            color=COLOR_SCHOOL_BOARD,
            message="На доске написано: «Сначала то, что имеет углы. Потом то, что не имеет. Потом то, что указывает вверх».",
            blocks_movement=True,
        )

        left_desk = InteractableObject(
            name="school_desk",
            rect=(120, 230, 180, 70),
            color=COLOR_SCHOOL_DESK,
            message="Парта. На ней выцарапаны слова: «не отвечай слишком быстро».",
            blocks_movement=True,
        )

        right_desk = InteractableObject(
            name="school_desk",
            rect=(660, 230, 180, 70),
            color=COLOR_SCHOOL_DESK,
            message="Парта. Здесь лежат чужие тетради без имён.",
            blocks_movement=True,
        )

        back_desk = InteractableObject(
            name="school_desk",
            rect=(390, 340, 180, 70),
            color=COLOR_SCHOOL_DESK,
            message="Парта. Кажется, она стоит не там, где должна.",
            blocks_movement=True,
        )

        symbol_panel = InteractableObject(
            name="symbol_panel",
            rect=(410, 170, 140, 45),
            color=COLOR_SYMBOL_PANEL,
            message="Панель с символами. На ней мерцают квадрат, круг и треугольник.",
            blocks_movement=False,
        )

        symbol_door = InteractableObject(
            name="symbol_door",
            rect=(420, 430, 120, 60),
            color=COLOR_SCHOOL_DOOR,
            message="Дверь закрыта. Рядом светятся три символа.",
            blocks_movement=True,
        )

        self.objects = [
            board,
            left_desk,
            right_desk,
            back_desk,
            symbol_panel,
        ]

        if progress is None or not progress.symbol_puzzle_solved:
            self.objects.append(symbol_door)
        else:
            opened_door = InteractableObject(
                name="opened_symbol_door",
                rect=(420, 430, 120, 60),
                color=COLOR_SCHOOL_DOOR,
                message="Дверь открыта. За ней снова видна станция.",
                blocks_movement=False,
            )
            self.objects.append(opened_door)

    def _create_final_station(self):
        self.floor_color = COLOR_FINAL_FLOOR
        self._create_base_walls(COLOR_FINAL_WALL)
        self._load_background("assets/locations/final_station.png")

        platform = InteractableObject(
            name="final_platform",
            rect=(90, 330, 780, 90),
            color=COLOR_FINAL_PLATFORM,
            message="Платформа стала тише. Кажется, станция ждёт ответа.",
            blocks_movement=False,
        )

        sign = InteractableObject(
            name="final_sign",
            rect=(300, 80, 360, 55),
            color=COLOR_FINAL_SIGN,
            message="На табло дрожат слова: «Следующая станция зависит от тебя».",
            blocks_movement=False,
        )

        conductor = InteractableObject(
            name="final_conductor",
            rect=(460, 220, 42, 58),
            color=COLOR_CONDUCTOR,
            message="Проводник ждёт у края платформы.",
            blocks_movement=True,
        )

        return_gate = InteractableObject(
            name="return_gate",
            rect=(250, 430, 140, 60),
            color=COLOR_FINAL_GATE,
            message="Проход назад. Отсюда будто слышен шум обычного города.",
            blocks_movement=True,
        )

        stay_gate = InteractableObject(
            name="stay_gate",
            rect=(570, 430, 140, 60),
            color=COLOR_FINAL_GATE,
            message="Проход дальше. За ним тихо светится станция без названия.",
            blocks_movement=True,
        )

        self.objects = [
            platform,
            sign,
            conductor,
            return_gate,
            stay_gate,
        ]

    def get_collision_rects(self):
        rects = []

        for wall in self.walls:
            rects.append(wall)

        for obj in self.objects:
            if obj.blocks_movement:
                rects.append(obj.rect)

        return rects

    def get_near_object(self, player_rect):
        interaction_zone = player_rect.inflate(70, 70)

        for obj in self.objects:
            if interaction_zone.colliderect(obj.rect):
                return obj

        return None
    
    def get_object_by_name(self, object_name):
        for obj in self.objects:
            if obj.name == object_name:
                return obj

        return None

    def draw(self, screen):
        game_area = pygame.Rect(0, 0, SCREEN_WIDTH, GAME_HEIGHT)

        if self.background_image is not None:
            screen.blit(self.background_image, (0, 0))
        else:
            pygame.draw.rect(screen, self.floor_color, game_area)

            for wall in self.walls:
                pygame.draw.rect(screen, self.wall_color, wall)

            for obj in self.objects:
                if obj.name in ("conductor", "final_conductor"):
                    continue

                obj.draw(screen)    