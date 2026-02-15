import math


class PhysicsEngine:
    """Физический движок для обработки коллизий"""

    @staticmethod
    def check_collision(sprite1, sprite2):
        """Проверка коллизии двух спрайтов"""
        dx = sprite1.center_x - sprite2.center_x
        dy = sprite1.center_y - sprite2.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance < (sprite1.width + sprite2.width) / 2

    @staticmethod
    def check_collision_with_list(sprite, sprite_list):
        """Проверка коллизии спрайта со списком"""
        collisions = []
        for other in sprite_list:
            if sprite != other and PhysicsEngine.check_collision(sprite, other):
                collisions.append(other)
        return collisions