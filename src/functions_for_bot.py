import telebot
from telebot import types
import csv
import random
import hashlib

token = '8065253218:AAHjv0WTW5qv2xp9tsT9EhXGXwqrnomXXpM'
bot = telebot.TeleBot(token)
callback_map = {}
buttons_per_page = 15  # 5 строки по 3 кнопок

def short_callback(value: str) -> str:
    # Генерируем короткий уникальный ключ (12 символов)
    return hashlib.md5(value.encode()).hexdigest()[:12]

#funcrion for updating genres
def check_genres():
    genre = []
    with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in (reader):
            # print(row['genres'])
            row_genre = row['genres'].split(',')
            for i in row_genre:
                if not(i in genre):
                    genre.append(i)
    f.close()
    return genre

genre = check_genres()

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
                types.InlineKeyboardButton(text='⛔️Выбор по категории', callback_data='user_choose'),
                types.InlineKeyboardButton(text='Подборки', callback_data='selection_menu'))
    return buttons

def selection_menu_b():
    buttons = types.InlineKeyboardMarkup()       
    buttons.add(types.InlineKeyboardButton(text='По жанрам', callback_data='sel_genre'), 
                types.InlineKeyboardButton(text='По актерам', callback_data='sel_actor'),
                types.InlineKeyboardButton(text='По периоду выпуска', callback_data='sel_year'),
                types.InlineKeyboardButton(text='Все фильмы', callback_data='sel_all_films'),
                types.InlineKeyboardButton(text='Все актеры', callback_data='sel_all_actor'),
                types.InlineKeyboardButton(text='Главное меню', callback_data='main')              
                )   
    return buttons


def selection_b(type_selection, page=0):
    types_of_sets = {
        'sel_genre': [10, 'genres'],
        'sel_actor': [11, 'actors'],
        'sel_year': [0, 'year'],
        'sel_all_films': [-1, 'none'],
        'sel_all_actor': [-11, 'actors']
    }

    markup = types.InlineKeyboardMarkup(row_width=3)

    if types_of_sets[type_selection][0] > 0:
        unique = set()
        buttons_data = []

        with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                values = row[types_of_sets[type_selection][1]].split(',')
                for val in values:
                    val = val.strip()
                    if val and val not in unique:
                        unique.add(val)
                        cb_data = short_callback(val)
                        callback_map[cb_data] = val
                        buttons_data.append((val, cb_data))

        total_pages = (len(buttons_data) + buttons_per_page - 1) // buttons_per_page
        start = page * buttons_per_page
        end = start + buttons_per_page
        current_buttons = buttons_data[start:end]

        for i in range(0, len(current_buttons), 3):
            row = [
                types.InlineKeyboardButton(text=name, callback_data=cb_data)
                for name, cb_data in current_buttons[i:i+3]
            ]
            markup.row(*row)

        # Кнопки навигации
        nav_buttons = [types.InlineKeyboardButton(text='Главное меню', callback_data='main')]
        if page > 0:
            nav_buttons.append(types.InlineKeyboardButton("⏮ Назад", callback_data=f"{type_selection}_page_{page-1}"))
        if page < total_pages - 1:
            nav_buttons.append(types.InlineKeyboardButton("⏭ Вперёд", callback_data=f"{type_selection}_page_{page+1}"))
        if nav_buttons:
            markup.row(*nav_buttons)

    return markup
 
def random_film_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add( types.InlineKeyboardButton(text='Выбрать другой фильм', callback_data='random_film'), 
                types.InlineKeyboardButton(text='Главное меню', callback_data='main'))
    return buttons  
def user_choose_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main'))
    return buttons    