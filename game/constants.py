# Константы игры
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Змейка"

# Размеры клеток
CELL_SIZE = 32  # попробовал 30 слишком мелко 32 норм
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # 32 клетки
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # 24 клетки

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)  # для оконтовки
GOLD = (255, 215, 0)  # золотой для рекорда

# Фон
BACKGROUND_COLOR = (25, 25, 50)  # темно синий норм смотрится
# BACKGROUND_COLOR = (0, 0, 0)  # пробовал черный скучно
GRID_COLOR = (60, 60, 90)  # серо голубой для сетки

# Цвета змейки
SNAKE_HEAD = (50, 255, 50)      # ярко зеленый
SNAKE_HEAD_OUTLINE = (0, 150, 0)  # темно зеленый для оконтовки головы
SNAKE_BODY = (0, 200, 0)        # зеленый
SNAKE_BODY_OUTLINE = (0, 100, 0)  # темно зеленый для оконтовки тела

# Цвета еды
RED = (255, 80, 80)             # красный
RED_OUTLINE = (150, 0, 0)
YELLOW = (255, 255, 100)         # желтый
YELLOW_OUTLINE = (150, 150, 0)
PURPLE = (180, 100, 255)         # фиолетовый
PURPLE_OUTLINE = (80, 0, 150)
ORANGE = (255, 150, 50)          # оранжевый
ORANGE_OUTLINE = (150, 80, 0)

# Состояния игры
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"  # надо еще паузу добавить потом

# Направления
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость игры
BASE_SPEED = 0.15  # начальная скорость
MIN_SPEED = 0.05   # максимальная скорость
SPEED_INCREASE = 0.0005  # плавное увеличение

# Файлы данных
HIGH_SCORE_FILE = "highscores.csv"
GAME_STATS_FILE = "stats.txt"