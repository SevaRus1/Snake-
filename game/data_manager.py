import csv
import os
from datetime import datetime


class DataManager:
    """Класс для управления данными игры"""

    def __init__(self):
        self.high_score_file = "highscores.csv"
        self.stats_file = "stats.txt"
        self.high_scores = []
        self.load_scores()

    def load_scores(self):
        """Загрузка рекордов из CSV"""
        self.high_scores = []

        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)  # Пропускаем заголовок
                    for row in reader:
                        if len(row) >= 3:
                            self.high_scores.append({
                                'score': int(row[0]),
                                'level': int(row[1]),
                                'date': row[2]
                            })
            except:
                pass

        # Сортируем по убыванию счета
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)

    def save_score(self, score, level, time_alive):
        """Сохранение результата в CSV"""
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        with open(self.high_score_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Если файл новый пишем заголовок
            if os.path.getsize(self.high_score_file) == 0:
                writer.writerow(['score', 'level', 'date'])

            writer.writerow([score, level, date])

        # Также сохраняем в текстовый файл статистику
        self.save_stats(score, level, time_alive)

        # Обновляем список рекордов
        self.load_scores()

    def save_stats(self, score, level, time_alive):
        """Сохранение статистики в текстовый файл"""
        with open(self.stats_file, 'a', encoding='utf-8') as file:
            file.write(f"\n--- Игра {datetime.now().strftime('%Y-%m-%d %H:%M')} ---\n")
            file.write(f"Счет: {score}\n")
            file.write(f"Уровень: {level}\n")
            file.write(f"Время жизни: {time_alive:.1f} сек\n")

    def get_high_score(self):
        """Получение максимального рекорда"""
        if self.high_scores:
            return self.high_scores[0]['score']
        return 0