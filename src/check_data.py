import csv

# Путь к файлу CSV
file_path = 'src/kinopoisk_top250_full.csv'

def get_unique_values():
    genres = set()
    actors = set()
    countries = set()

    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Обрабатываем жанры
            row_genres = row['genres'].split(',')
            genres.update([g.strip() for g in row_genres])  # добавляем уникальные жанры

            # Обрабатываем актеров
            row_actors = row['actors'].split(',')
            actors.update([a.strip() for a in row_actors])  # добавляем уникальных актеров

            # Обрабатываем страны
            row_countries = row['countries'].split(',')
            countries.update([c.strip() for c in row_countries])  # добавляем уникальные страны

    # Преобразуем наборы в отсортированные списки
    return sorted(list(genres)), sorted(list(actors)), sorted(list(countries))

# Получаем все уникальные значения
genres, actors, countries = get_unique_values()

# Выводим результаты
# print("Жанры:", genres)
print("Актеры:", actors, len(actors))
# print("Страны:", countries)
