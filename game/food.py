import arcade
import random
import math
import time
from game.constants import *


class Food:
    """Класс еды """

    def __init__(self, x, y, food_type="normal"):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.food_type = food_type
        self.points = 1 if food_type == "normal" else 3  # для бонусной 3 очка
        self.grow_amount = 1 if food_type == "normal" else 2  # специальная еда дает +2 длины

        # Выбираем цвет в зависимости от типа
        if food_type == "normal":
            self.color = RED
            self.outline = RED_OUTLINE
        elif food_type == "special":
            self.color = YELLOW
            self.outline = YELLOW_OUTLINE
        elif food_type == "bonus":
            self.color = PURPLE
            self.outline = PURPLE_OUTLINE
        else:
            self.color = ORANGE
            self.outline = ORANGE_OUTLINE

        # Для анимации
        self.pulse_offset = random.uniform(0, 2 * math.pi)

    def draw(self):
        """Отрисовкаеды"""
        # анимация пульсации
        pulse = math.sin(time.time() * 3 + self.pulse_offset) * 0.1 + 1
        size = CELL_SIZE // 2 * pulse

        # Основной круг
        arcade.draw_circle_filled(self.x, self.y, size, self.color)

        # Оконтовка добавил позже стало лучше смотреться
        arcade.draw_circle_outline(self.x, self.y, size, self.outline, 1)

        arcade.draw_circle_filled(
            self.x - size // 3,
            self.y + size // 3,
            size // 4,
            (255, 255, 255, 100)
        )