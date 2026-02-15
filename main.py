import arcade
from game.game_view import SnakeGameView


def main():
    """Главная функция запуска игры"""
    window = arcade.Window(
        width=1024,
        height=768,
        title="Змейка",
        center_window=True
    )

    start_view = SnakeGameView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()