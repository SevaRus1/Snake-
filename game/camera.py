import arcade
from game.constants import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """Простая камера"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0

    def use(self):
        pass

    def move_to(self, x, y):
        """Движение камеры к точке"""
        self.offset_x = x - self.width // 2
        self.offset_y = y - self.height // 2

        # Ограничиваем смещение границами поля
        max_x = GRID_WIDTH * CELL_SIZE - self.width
        max_y = GRID_HEIGHT * CELL_SIZE - self.height

        self.offset_x = max(0, min(self.offset_x, max_x))
        self.offset_y = max(0, min(self.offset_y, max_y))

    def reset(self):
        """Сброс камеры"""
        self.offset_x = 0
        self.offset_y = 0