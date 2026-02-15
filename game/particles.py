import arcade
import random
import math
from game.constants import *


class Particle(arcade.Sprite):
    """Класс частицы"""

    def __init__(self, x, y, color, velocity_x=0, velocity_y=0, lifetime=1.0):
        super().__init__()

        self.texture = arcade.make_soft_square_texture(
            random.randint(2, 6),
            color,
            outer_alpha=0
        )

        self.center_x = x
        self.center_y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.age = 0
        self.alpha = 255

    def update(self, delta_time):
        """Обновление частицы"""
        self.age += delta_time

        if self.age >= self.lifetime:
            self.remove_from_sprite_lists()
            return

        # Движение
        self.center_x += self.velocity_x * delta_time * 60
        self.center_y += self.velocity_y * delta_time * 60

        # Замедление
        self.velocity_x *= 0.95
        self.velocity_y *= 0.95

        # Изменение прозрачности
        self.alpha = int(255 * (1 - self.age / self.lifetime))
        self.color = (self.color[0], self.color[1], self.color[2], self.alpha)


class ParticleSystem:
    """Система частиц"""

    def __init__(self):
        self.particles = arcade.SpriteList()
        self.stars = []
        self.init_stars()

    def init_stars(self):
        """Инициализация фоновых звезд"""
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, 1024),
                'y': random.randint(0, 768),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5)
            })

    def add_burst(self, x, y, color):
        """Добавление взрыва частиц"""
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)

            particle = Particle(
                x, y, color,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                random.uniform(0.5, 1.0)
            )
            self.particles.append(particle)

    def add_explosion(self, x, y):
        """Добавление большого взрыва"""
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)

            color = random.choice([RED, ORANGE, YELLOW])

            particle = Particle(
                x, y, color,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                random.uniform(0.8, 1.5)
            )
            self.particles.append(particle)

    def add_trail(self, x, y, color):
        """Добавление следа"""
        particle = Particle(
            x, y, color,
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            0.3
        )
        self.particles.append(particle)

    def update(self, delta_time):
        """Обновление частиц"""
        self.particles.update(delta_time)

        # Обновление звезд
        for star in self.stars:
            star['y'] -= star['speed']
            if star['y'] < 0:
                star['y'] = 768
                star['x'] = random.randint(0, 1024)

    def draw(self):
        """Отрисовка частиц"""
        self.particles.draw()

    def draw_background_stars(self):
        """Отрисовка фоновых звезд"""
        for star in self.stars:
            arcade.draw_circle_filled(
                star['x'],
                star['y'],
                star['size'],
                WHITE
            )