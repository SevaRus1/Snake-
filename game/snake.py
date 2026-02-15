import arcade
import math
from game.constants import *


class SnakeSegment:
    """ тела змейки """

    def __init__(self, x, y, color, outline_color, is_head=False):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.color = color
        self.outline_color = outline_color
        self.is_head = is_head
        self.width = CELL_SIZE - 2
        self.height = CELL_SIZE - 2

    def draw(self, direction=None):
        # Рисуем основной квадрат
        arcade.draw_rect_filled(
            arcade.XYWH(self.x, self.y, self.width, self.height),
            self.color
        )

        # Рисуем оконтовку
        arcade.draw_rect_outline(
            arcade.XYWH(self.x, self.y, self.width, self.height),
            self.outline_color,
            1
        )

        # Глаза только для головы
        if self.is_head and direction:
            eye_size = 4
            eye_offset = 8  # чет далековато глаза может уменьшить

            # Белки глаз
            if direction == RIGHT:
                arcade.draw_circle_filled(self.x + eye_offset, self.y + 5, eye_size, WHITE)
                arcade.draw_circle_filled(self.x + eye_offset, self.y - 5, eye_size, WHITE)
                # Зрачки
                arcade.draw_circle_filled(self.x + eye_offset + 2, self.y + 5, eye_size // 2, BLACK)
                arcade.draw_circle_filled(self.x + eye_offset + 2, self.y - 5, eye_size // 2, BLACK)
                # Оконтовка глаз надо было сразу добавить
                arcade.draw_circle_outline(self.x + eye_offset, self.y + 5, eye_size, LIGHT_GRAY, 1)
                arcade.draw_circle_outline(self.x + eye_offset, self.y - 5, eye_size, LIGHT_GRAY, 1)
            elif direction == LEFT:
                arcade.draw_circle_filled(self.x - eye_offset, self.y + 5, eye_size, WHITE)
                arcade.draw_circle_filled(self.x - eye_offset, self.y - 5, eye_size, WHITE)
                arcade.draw_circle_filled(self.x - eye_offset - 2, self.y + 5, eye_size // 2, BLACK)
                arcade.draw_circle_filled(self.x - eye_offset - 2, self.y - 5, eye_size // 2, BLACK)
                arcade.draw_circle_outline(self.x - eye_offset, self.y + 5, eye_size, LIGHT_GRAY, 1)
                arcade.draw_circle_outline(self.x - eye_offset, self.y - 5, eye_size, LIGHT_GRAY, 1)
            elif direction == UP:
                arcade.draw_circle_filled(self.x + 5, self.y + eye_offset, eye_size, WHITE)
                arcade.draw_circle_filled(self.x - 5, self.y + eye_offset, eye_size, WHITE)
                arcade.draw_circle_filled(self.x + 5, self.y + eye_offset + 2, eye_size // 2, BLACK)
                arcade.draw_circle_filled(self.x - 5, self.y + eye_offset + 2, eye_size // 2, BLACK)
                arcade.draw_circle_outline(self.x + 5, self.y + eye_offset, eye_size, LIGHT_GRAY, 1)
                arcade.draw_circle_outline(self.x - 5, self.y + eye_offset, eye_size, LIGHT_GRAY, 1)
            elif direction == DOWN:
                arcade.draw_circle_filled(self.x + 5, self.y - eye_offset, eye_size, WHITE)
                arcade.draw_circle_filled(self.x - 5, self.y - eye_offset, eye_size, WHITE)
                arcade.draw_circle_filled(self.x + 5, self.y - eye_offset - 2, eye_size // 2, BLACK)
                arcade.draw_circle_filled(self.x - 5, self.y - eye_offset - 2, eye_size // 2, BLACK)
                arcade.draw_circle_outline(self.x + 5, self.y - eye_offset, eye_size, LIGHT_GRAY, 1)
                arcade.draw_circle_outline(self.x - 5, self.y - eye_offset, eye_size, LIGHT_GRAY, 1)


class Snake:
    """Класс змейки"""

    def __init__(self, start_x=10, start_y=10):
        self.segments = []
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_flag = False  # тупил с этим флагом час

        # Создаем начальную змейку 3 сегмента
        for i in range(3):
            if i == 0:
                color = SNAKE_HEAD
                outline = SNAKE_HEAD_OUTLINE
            else:
                color = SNAKE_BODY
                outline = SNAKE_BODY_OUTLINE
            segment = SnakeSegment(start_x - i, start_y, color, outline, i == 0)
            self.segments.append(segment)

        self.head = self.segments[0]

    def change_direction(self, new_direction):
        """Изменение направления движения"""
        # Запрещаем разворот на 180 градусов
        if (new_direction[0] != -self.direction[0] or
                new_direction[1] != -self.direction[1]):
            self.next_direction = new_direction
        # else:
        #     print("нельзя развернуться")  # для отладки

    def move(self):
        """Движение змейки"""
        self.direction = self.next_direction

        # Получаем позицию головы в клетках
        head_x = int(self.head.x // CELL_SIZE)
        head_y = int(self.head.y // CELL_SIZE)

        # Новая позиция головы
        new_head_x = head_x + self.direction[0]
        new_head_y = head_y + self.direction[1]

        # Создаем новую голову
        new_head = SnakeSegment(new_head_x, new_head_y, SNAKE_HEAD, SNAKE_HEAD_OUTLINE, True)
        self.segments.insert(0, new_head)

        # Если не нужно расти удаляем хвост
        if not self.grow_flag:
            self.segments.pop()
        else:
            self.grow_flag = False

        self.head = self.segments[0]

    def grow(self):
        """Увеличение длины змейки"""
        self.grow_flag = True  # вот тут была ошибка забыл True поставить

    def check_self_collision(self):
        """Проверка столкновения с собой"""
        head = self.segments[0]
        for segment in self.segments[1:]:
            distance = math.sqrt((head.x - segment.x) ** 2 + (head.y - segment.y) ** 2)
            if distance < CELL_SIZE // 2:
                return True
        return False

    def check_wall_collision(self):
        """Проверка столкновения со стенами"""
        head = self.segments[0]
        x = head.x // CELL_SIZE
        y = head.y // CELL_SIZE

        return (x < 0 or x >= GRID_WIDTH or
                y < 0 or y >= GRID_HEIGHT)

    def draw(self):
        """Отрисовка змейки"""
        for i, segment in enumerate(self.segments):
            # Для головы передаем направление
            if i == 0:
                segment.draw(self.direction)
            else:
                segment.draw()