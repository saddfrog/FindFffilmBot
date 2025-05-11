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
time = ['0', '60', '120', '180']
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
    time = filters.get('time', "всё")
    rating = filters.get('rating', "всё")

    return (f"🎯 *Текущие фильтры:*\n"
            f"Год выпуска: {year}\n"
            f"Жанр: {genre}\n"
            f"Страна: {country}\n"
            f"Возрастной рейтинг: {age}\n"
            f"Актёр: {actor}\n"
            f"Хронометраж фильма: {time}\n"
            f"Рейтинг: {rating}")


buttons_per_page = 15  # 5 строки по 3 кнопок

# Функция для создания кнопок для фильтров
def filter_menu_b():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Год выпуска", callback_data="choose_year"),
        types.InlineKeyboardButton("Страна", callback_data="choose_country"),
        types.InlineKeyboardButton("Рейтинг", callback_data="choose_rating"),

    )
    markup.add(
        types.InlineKeyboardButton("Актёр", callback_data="choose_actor"),
        types.InlineKeyboardButton("Хронометраж", callback_data="choose_time"),
        types.InlineKeyboardButton("Жанр", callback_data="choose_genre"),

    )
    markup.add(
        types.InlineKeyboardButton("🎬 Показать фильмы", callback_data="show_filtered"),
        types.InlineKeyboardButton("🔄 Сбросить фильтры", callback_data='reset_filters'),
    )
    markup.add(
        types.InlineKeyboardButton("🏠 Главное меню", callback_data="start")
    )
    return markup
  

def filtred_films(chat_id, results):
    film = random.choice(results)
    film_desc = film['description']
    if len(film_desc.split()) > 80 or len(film_desc) > 500:
        film_desc = ' '.join(film_desc.split()[:50])
    caption_f = (
    f"🎬 *Ваш фильм*: `{film['title_ru']}` 🎞 `{film['title_original']}`\n"
    f"📝 *Описание*: {film_desc}\n\n"
    f"⭐️ *КП*: {film['rating_kp']} | 🌟 *IMDb*: {film['rating_imdb']} | 🔞 *Возраст*: {film['age_rating']}\n"
    f"🎭 *Актеры*: {film['actors']}\n"
    f"🎬 *Режиссеры*: {film['directors']} | 🌍 *Страна*: {film['countries']}\n"
    f"📅 *Год*: {film['year']} | ⏳ *Хронометраж*: {film['film_length']} мин\n"
    f"🎭 *Жанры*: {film['genres']}"
    )
    print(caption_f)
    try:
        bot.send_photo(chat_id,photo=film['poster_url'], caption=caption_f, parse_mode="MARKDOWN")
        # summary = format_filter_summary(user_filters[chat_id])        
        # bot.send_message(chat_id, text=f"{summary}", parse_mode="MARKDOWN", reply_markup=filter_menu_b())

    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

def short_callback(value: str) -> str:
    # Генерируем короткий уникальный ключ (12 символов)
    return hashlib.md5(value.encode()).hexdigest()[:12]

def start_b():
    markup = types.InlineKeyboardMarkup()
    markup.add(
                types.InlineKeyboardButton(text='Выбор по категории', callback_data='user_choose'),
                types.InlineKeyboardButton(text='Случайный фильм', callback_data='random_film'))
    
    markup.add(types.InlineKeyboardButton(text='От разработчиков', callback_data='from_developers'))
    return markup

def user_choose_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(types.InlineKeyboardButton(text='Главное меню', callback_data='start'))
    return buttons    

def random_menu_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(
        types.InlineKeyboardButton(text='Другой фильм', callback_data='random_film'),         
        types.InlineKeyboardButton(text='Выбор по категории', callback_data='user_choose')
                )
    buttons.add(types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='start'))
    return buttons   
