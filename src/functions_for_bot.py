import telebot
from telebot import types
import csv
import random
import hashlib

token = '8065253218:AAHjv0WTW5qv2xp9tsT9EhXGXwqrnomXXpM'
bot = telebot.TeleBot(token)
callback_map = {}
user_filters = {}  # chat_id: { 'year': '1990', 'genre': 'комедия', ... }

years = ['1980', '1990', '2000', '2010', '2020']
ages = ['0+', '6+', '12+', '16+', '18+']

genre = ['аниме', 'биография', 'боевик', 'вестерн', 'военный', 'детектив', 'драма', 'история', 'комедия', 
         'криминал', 'мелодрама', 'музыка', 'мультфильм', 'мюзикл', 'приключения', 'семейный', 'спорт', 
         'триллер', 'ужасы', 'фантастика', 'фэнтези'
         ]

countries = ['Австралия', 'Австрия', 'Беларусь', 'Бельгия', 'Болгария', 'Великобритания', 
             'Венгрия', 'Гамбия', 'Германия', 'Гонконг', 'Дания', 'Индия', 'Иордания', 'Испания', 'Италия', 
             'Канада', 'Китай', 'Корея Южная', 'Латвия', 'Мальта', 'Марокко', 'Мексика', 'Нидерланды', 
             'Новая Зеландия', 'Норвегия', 'ОАЭ', 'Польша', 'Россия', 'СССР', 'США', 'Сербия', 'Таиланд', 
             'Финляндия', 'Франция', 'Чехия', 'Швейцария', 'Швеция', 'Япония'
             ]

actors = [
    'Александр Абдулов', 'Александр Демидов', 'Алексей Бардуков', 'Алексей Булдаков', 'Алексей Кравченко',
    'Алиса Фрейндлих', 'Анатолий Папанов', 'Андрей Миронов', 'Андрей Мягков', 'Анна Синякина',
    'Анна Фрил', 'Артём Меркулов', 'Бен Аффлек', 'Бенедикт Камбербэтч', 'Брайан Кокс',
    'Брэд Питт', 'Брэдли Купер', 'Брюс Уиллис', 'Валентин Гафт', 'Василий Ливанов',
    'Виктор Сухоруков', 'Владимир Машков', 'Владимир Меньшов', 'Гарри Олдман', 'Гоша Куценко',
    'Даниэль Брюль', 'Джаред Лето', 'Джейк Джилленхол', 'Джейми Ли Кёртис', 'Джеймс Макэвой',
    'Джон Траволта', 'Джонни Депп', 'Джош Бролин', 'Джозеф Гордон-Левитт', 'Джулия Робертс',
    'Джулия Уолтерс', 'Джонни Флинн', 'Евгений Миронов', 'Евгения Глотова', 'Евгения Симонова',
    'Екатерина Васильева', 'Екатерина Маркова', 'Елена Проклова', 'Жан Рено', 'Кейт Бланшетт',
    'Кевин Спейси', 'Крис Хемсворт', 'Крис Эванс', 'Кристофер Ллойд', 'Кристофер Пламмер'
        ]


def format_filter_summary(filters):
    year = f"{filters['year']}–{int(filters['year'])+9}" if 'year' in filters else "всё"
    genre = filters.get('genre', "всё")
    country = filters.get('country', "всё")
    age = filters.get('age', "всё")
    actor = filters.get('actor', "всё")
    return (f"🎯 *Текущие фильтры:*\n"
            f"Год выпуска: {year}\n"
            f"Жанр: {genre}\n"
            f"Страна: {country}\n"
            f"Возрастной рейтинг: {age}\n"
            f"Актёр: {actor}")


buttons_per_page = 15  # 5 строки по 3 кнопок

# Функция для создания кнопок для фильтров
def filter_menu_b():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Год выпуска", callback_data="choose_year"),
        types.InlineKeyboardButton("Жанр", callback_data="choose_genre"),
        types.InlineKeyboardButton("Страна", callback_data="choose_country"),
    )
    markup.add(
        types.InlineKeyboardButton("Возрастной рейтинг", callback_data="choose_age"),
        types.InlineKeyboardButton("Актёр", callback_data="choose_actor"),
    )
    markup.add(
        types.InlineKeyboardButton("🎬 Показать фильмы", callback_data="show_filtered"),
        types.InlineKeyboardButton("🔄 Сбросить фильтры", callback_data='reset_filters'),
    )
    markup.add(
        types.InlineKeyboardButton("🏠 Главное меню", callback_data="main")
    )
    return markup


# Функции фильтрации (с учетом структуры БД)
def filter_by_year(year):
    films = []
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if year in row['year']:
                films.append(row)
    return films

def filter_by_country(country):
    films = []
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if country in row['countries']:
                films.append(row)
    return films

def filter_by_age(age_limit):
    films = []
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if age_limit in row['age_rating']:
                films.append(row)
    return films

def filter_by_actor(actor):
    films = []
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if actor in row['actors']:
                films.append(row)
    return films

def filter_by_genre(genre):
    films = []
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if genre in row['genres']:
                films.append(row)
    return films

# Функция для отправки отфильтрованных фильмов
def send_filtered_films(chat_id, films):
    if films:
        for film in films:
            bot.send_photo(chat_id, photo=film['poster_url'], caption=f"🎬*Ваш фильм*: `{film['title_ru']}`\n\n*Описание фильма*: {film['description']}\n\n *Возрастной рейтинг*: {film['age_rating']}", parse_mode="MARKDOWN", reply_markup=random_film_b())
    else:
        bot.send_message(chat_id=chat_id, text="Не найдено фильмов по выбранному фильтру. Попробуйте другой фильтр.")
    
def filtred_films(chat_id, results):
    film = random.choice(results)
    bot.send_photo(chat_id, photo=film['poster_url'], 
                   caption=f"🎬*Ваш фильм*: `{film['title_ru']}`\n\n*Описание фильма*: {film['description']}\n\n *Возрастной рейтинг*: {film['age_rating']}", 
                   parse_mode="MARKDOWN", reply_markup=filter_menu_b())


def short_callback(value: str) -> str:
    # Генерируем короткий уникальный ключ (12 символов)
    return hashlib.md5(value.encode()).hexdigest()[:12]

def random_film():
    film = ""
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        film_ind = random.randint(1, 250)
        for ind_reader, row in enumerate(reader):
            if ind_reader == film_ind:
                # print(row[0])
                film = row
                break
    f.close()
    return film

def del_prev_buttons(call):
    bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')

def main_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(types.InlineKeyboardButton(text='Случайный фильм', callback_data='random_film'), 
                types.InlineKeyboardButton(text='TESTING: Выбор по категории', callback_data='user_choose'))
                # types.InlineKeyboardButton(text='Подборки', callback_data='selection_menu'))
    return buttons

def random_film_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add( types.InlineKeyboardButton(text='Выбрать другой фильм', callback_data='random_film'), 
                types.InlineKeyboardButton(text='Главное меню', callback_data='main'))
    return buttons  
def user_choose_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main'))
    return buttons    