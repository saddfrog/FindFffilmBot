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
# genres, actors, countries = get_unique_values()

# Выводим результаты
# print("Жанры:", genres)
# print("Актеры:", actors, len(actors))
# print("Страны:", countries)
st = 'Идёт третий год Войн клонов. Галактическая Республика, некогда бывшая спокойным и гармоничным государством, превратилась в поле битвы между армиями клонов, возглавляемых канцлером Палпатином, и армадами дроидов, которых ведёт граф Дуку, тёмный лорд ситхов. Республика медленно погружается во тьму. Лишь рыцари-джедаи, защитники мира и справедливости, могут противостоять злу, которое вскоре поглотит галактику. Но настоящая битва идёт в душе у молодого рыцаря-джедая Энакина, который разрывается между долгом джедая и любовью к своей жене, сенатору Падме Амидале. И от того, какое чувство в нём победит, зависит будущее всего мира....'
print(len(st))


