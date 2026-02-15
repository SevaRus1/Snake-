import arcade
import random
import time
import math
from game.constants import *
from game.snake import Snake
from game.food import Food
from game.particles import ParticleSystem
from game.camera import Camera
from game.physics import PhysicsEngine
from game.data_manager import DataManager


class SnakeGameView(arcade.View):
    """Основной класс игры с управлением состояниями"""

    def __init__(self):
        super().__init__()

        # Менеджеры и состояния
        self.current_state = STATE_START
        self.data_manager = DataManager()
        self.particle_system = ParticleSystem()
        self.physics_engine = PhysicsEngine()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Звуки
        self.eat_sound = None
        self.game_over_sound = None
        self.start_sound = None
        self.background_music = None
        self.background_player = None  # для управления музыкой

        # Игровые объекты
        self.snake = None
        self.food_list = []

        # Счет и статистика
        self.score = 0
        self.foods_eaten = 0
        self.time_alive = 0

        # Таймеры
        self.update_timer = 0
        self.food_spawn_timer = 0
        self.speed_timer = 0

        # Для плавного изменения скорости
        self.current_speed = BASE_SPEED
        self.target_speed = BASE_SPEED

        # Загружаем звуки
        self.load_sounds()

        # Текст для UI
        self.setup_text()

    def load_sounds(self):
        """Загрузка звуков из файлов"""
        try:
            self.eat_sound = arcade.load_sound("assets/sounds/eat.wav")
            print("Звук еды загружен")
        except:
            print("Не удалось загрузить звук еды")  # TODO скачать нормальный звук

        try:
            self.game_over_sound = arcade.load_sound("assets/sounds/game_over.wav")
            print("Звук game over загружен")
        except:
            print("Не удалось загрузить звук game over")

        try:
            self.start_sound = arcade.load_sound("assets/sounds/start.wav")
            print("Звук старта загружен")
        except:
            print("Не удалось загрузить звук старта")

        try:
            # ЗДЕСЬ ТВОЯ МУЗЫКА
            self.background_music = arcade.load_sound("assets/sounds/background.mp3")
            print("Фоновая музыка загружена")
        except:
            print("Не удалось загрузить фоновую музыку")  # не грузится потом разберусь

    def on_show_view(self):
        """Вызывается при показе view"""
        arcade.set_background_color(BACKGROUND_COLOR)

        # Запускаем фоновую музыку при показе стартового экрана
        if self.current_state == STATE_START and self.background_music:
            self.background_player = self.background_music.play(volume=0.3, loop=True)

    def on_hide_view(self):
        """Вызывается при скрытии view"""
        # Останавливаем музыку при выходе
        if self.background_player:
            arcade.stop_sound(self.background_player)
            self.background_player = None

    def setup_text(self):
        """Настройка элементов интерфейса"""
        self.start_title = arcade.Text(
            "SNAKE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            WHITE,
            72,
            anchor_x="center",
            anchor_y="center"
        )

        self.start_subtitle = arcade.Text(
            "CLASSIC",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 40,
            (200, 200, 200),
            36,
            anchor_x="center",
            anchor_y="center"
        )

        self.start_instruction = arcade.Text(
            "НАЖМИТЕ ПРОБЕЛ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            (150, 255, 150),
            24,
            anchor_x="center",
            anchor_y="center"
        )

        self.high_score_display = arcade.Text(
            f"РЕКОРД: {self.data_manager.get_high_score()}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 150,
            GOLD,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        # UI элементы
        self.score_text = arcade.Text("", 20, SCREEN_HEIGHT - 40, WHITE, 18)
        self.speed_text = arcade.Text("", 20, SCREEN_HEIGHT - 65, (150, 255, 150), 16)

    def setup_game(self):
        """Настройка новой игры"""
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food_list = []
        self.score = 0
        self.foods_eaten = 0
        self.time_alive = 0
        self.current_speed = BASE_SPEED
        self.target_speed = BASE_SPEED
        self.speed_timer = 0

        # Останавливаем фоновую музыку во время игры
        if self.background_player:
            arcade.stop_sound(self.background_player)
            self.background_player = None

        # Создаем первую еду
        self.spawn_food()

        # Сбрасываем камеру
        self.camera.reset()

    def spawn_food(self):
        """Создание новой еды"""
        if len(self.food_list) < 3:  # чтобы не слишком много еды было
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            # Проверяем не занято ли место змейкой
            occupied = False
            if self.snake:
                for segment in self.snake.segments:
                    seg_x = int(segment.x // CELL_SIZE)
                    seg_y = int(segment.y // CELL_SIZE)
                    if seg_x == x and seg_y == y:
                        occupied = True
                        break

            if not occupied:
                rand = random.random()
                if rand < 0.7:  # 70 процентов обычная еда
                    food_type = "normal"
                elif rand < 0.9:  # 20 процентов специальная
                    food_type = "special"
                else:  # 10 процентов бонусная
                    food_type = "bonus"

                food = Food(x, y, food_type)
                self.food_list.append(food)

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        if self.current_state == STATE_START:
            self.draw_start_screen()
        elif self.current_state == STATE_PLAYING:
            self.draw_game()
        elif self.current_state == STATE_GAME_OVER:
            self.draw_game_over_screen()

    def draw_start_screen(self):
        """Отрисовка стартового экрана"""
        # Затемнение
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, 0, 0, 150)
        )

        self.start_title.draw()
        self.start_subtitle.draw()
        self.start_instruction.draw()
        self.high_score_display.draw()

        # Простая анимированная змейка
        for i in range(5):
            x = SCREEN_WIDTH // 2 - 80 + i * 40
            y = SCREEN_HEIGHT // 2 - 200 + math.sin(time.time() * 2 + i) * 10
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            outline = SNAKE_HEAD_OUTLINE if i == 0 else SNAKE_BODY_OUTLINE
            arcade.draw_rect_filled(
                arcade.XYWH(x, y, 30, 30),
                color
            )
            arcade.draw_rect_outline(
                arcade.XYWH(x, y, 30, 30),
                outline,
                1
            )

    def draw_game(self):
        """Отрисовка игрового процесса"""
        # Рисуем сетку
        self.draw_grid()

        # Рисуем объекты
        for food in self.food_list:
            food.draw()

        if self.snake:
            self.snake.draw()

        # Рисуем частицы
        self.particle_system.draw()

        # Рисуем UI
        self.draw_ui()

    def draw_grid(self):
        """Отрисовка сетки"""
        for x in range(GRID_WIDTH + 1):
            arcade.draw_line(
                x * CELL_SIZE - self.camera.offset_x,
                0 - self.camera.offset_y,
                x * CELL_SIZE - self.camera.offset_x,
                GRID_HEIGHT * CELL_SIZE - self.camera.offset_y,
                GRID_COLOR,
                1
            )

        for y in range(GRID_HEIGHT + 1):
            arcade.draw_line(
                0 - self.camera.offset_x,
                y * CELL_SIZE - self.camera.offset_y,
                GRID_WIDTH * CELL_SIZE - self.camera.offset_x,
                y * CELL_SIZE - self.camera.offset_y,
                GRID_COLOR,
                1
            )

    def draw_ui(self):
        """Отрисовка интерфейса"""
        self.score_text.text = f"СЧЕТ: {self.score}"
        self.score_text.draw()

        # Показываем скорость
        speed_percent = int((1 - (self.current_speed - MIN_SPEED) / (BASE_SPEED - MIN_SPEED)) * 100)
        self.speed_text.text = f"СКОРОСТЬ: {speed_percent}%"
        self.speed_text.draw()

    def draw_game_over_screen(self):
        """Отрисовка финального экрана"""
        # Затемнение фона
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, 0, 0, 200)
        )

        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            RED, 64,
            anchor_x="center"
        )

        arcade.draw_text(
            f"СЧЕТ: {self.score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 30,
            WHITE, 36,
            anchor_x="center"
        )

        arcade.draw_text(
            f"СЪЕДЕНО: {self.foods_eaten}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 10,
            WHITE, 24,
            anchor_x="center"
        )

        high_score = self.data_manager.get_high_score()
        if self.score > high_score:
            arcade.draw_text(
                "НОВЫЙ РЕКОРД",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                GOLD, 28,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                f"РЕКОРД: {high_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                GOLD, 24,
                anchor_x="center"
            )

        arcade.draw_text(
            "R РЕСТАРТ     ESC ВЫХОД",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 120,
            WHITE, 18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if self.current_state == STATE_START:
            if key == arcade.key.SPACE:
                # Звук старта
                if self.start_sound:
                    self.start_sound.play(volume=0.5)
                self.current_state = STATE_PLAYING
                self.setup_game()

        elif self.current_state == STATE_PLAYING:
            if self.snake:
                if key == arcade.key.UP:
                    self.snake.change_direction(UP)
                elif key == arcade.key.DOWN:
                    self.snake.change_direction(DOWN)
                elif key == arcade.key.LEFT:
                    self.snake.change_direction(LEFT)
                elif key == arcade.key.RIGHT:
                    self.snake.change_direction(RIGHT)

        elif self.current_state == STATE_GAME_OVER:
            if key == arcade.key.R:
                self.current_state = STATE_PLAYING
                self.setup_game()
            elif key == arcade.key.ESCAPE:
                self.current_state = STATE_START
                # Возвращаем фоновую музыку при выходе в меню
                if self.background_music and not self.background_player:
                    self.background_player = self.background_music.play(volume=0.3, loop=True)

    def on_update(self, delta_time):
        """Обновление игры"""
        self.update_timer += delta_time
        self.food_spawn_timer += delta_time
        self.speed_timer += delta_time

        if self.current_state == STATE_PLAYING:
            self.time_alive += delta_time

            # Обновление частиц
            self.particle_system.update(delta_time)

            # Плавное увеличение скорости со временем
            if self.speed_timer >= 1.0:  # Каждую секунду
                self.speed_timer = 0
                if self.current_speed > MIN_SPEED:
                    self.target_speed = max(MIN_SPEED, self.target_speed - 0.0001)
                    # print(f"скорость {self.current_speed}")  # для отладки

            # Плавное изменение скорости
            if abs(self.current_speed - self.target_speed) > 0.001:
                self.current_speed += (self.target_speed - self.current_speed) * 0.1

            # Движение змейки
            if self.update_timer >= self.current_speed:
                self.update_timer = 0

                if self.snake:
                    self.snake.move()

                    # Проверка коллизий с едой
                    self.check_food_collisions()

                    # Проверка столкновений
                    if self.check_collisions():
                        self.game_over()

            # Автоматическое создание еды
            if self.food_spawn_timer >= 3.0:
                self.food_spawn_timer = 0
                self.spawn_food()

            # Обновление камеры
            if self.snake and self.snake.head:
                self.camera.move_to(
                    self.snake.head.x,
                    self.snake.head.y
                )

    def check_food_collisions(self):
        """Проверка столкновения с едой"""
        if not self.snake or not self.snake.head:
            return

        head = self.snake.head
        for food in self.food_list[:]:
            distance = math.sqrt((head.x - food.x) ** 2 + (head.y - food.y) ** 2)
            if distance < CELL_SIZE // 2:
                # Добавляем очки
                self.score += food.points
                self.foods_eaten += 1

                # Звук поедания
                if self.eat_sound:
                    self.eat_sound.play(volume=0.3)

                # Увеличиваем змейку
                for _ in range(food.grow_amount):
                    self.snake.grow()

                # Создаем частицы
                self.particle_system.add_burst(
                    food.x,
                    food.y,
                    food.color
                )

                # Удаляем съеденную еду
                self.food_list.remove(food)
                self.spawn_food()

    def check_collisions(self):
        """Проверка всех коллизий"""
        if not self.snake:
            return False

        if self.snake.check_self_collision():
            # print("самоубийство")  # для отладки
            return True

        if self.snake.check_wall_collision():
            # print("врезался в стену")  # для отладки
            return True

        return False

    def game_over(self):
        """Завершение игры"""
        self.current_state = STATE_GAME_OVER

        # Звук game over
        if self.game_over_sound:
            self.game_over_sound.play(volume=0.5)

        # Сохраняем результат
        self.data_manager.save_score(self.score, 1, self.time_alive)

        # Обновляем рекорд в UI
        self.high_score_display.text = f"РЕКОРД: {self.data_manager.get_high_score()}"

        # Создаем финальные частицы
        if self.snake:
            for segment in self.snake.segments:
                self.particle_system.add_explosion(
                    segment.x,
                    segment.y
                )