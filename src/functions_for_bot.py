import telebot
from telebot import types
import csv
import random

token = '8065253218:AAHjv0WTW5qv2xp9tsT9EhXGXwqrnomXXpM'
bot = telebot.TeleBot(token)

def random_film():
    film = 'none'
    with open('src/films.csv') as f:
        reader = csv.reader(f)
        ind_reader = 0
        film_ind = random.randint(0, 4804)
        for row in reader:
            if ind_reader == film_ind:  
                film = row[1]
                break
            ind_reader += 1
    f.close()
    print(film)
    return film

def del_prev_buttons(call):
    bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')

def main_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(types.InlineKeyboardButton(text='Случайный фильм', callback_data='random_film'), types.InlineKeyboardButton(text='⛔️Выбор по категории', callback_data='user_choose'))
    return buttons
def random_film_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add( types.InlineKeyboardButton(text='Выбрать другой фильм', callback_data='random_film'), types.InlineKeyboardButton(text='Главное меню', callback_data='main'))
    return buttons  
def user_choose_b():
    buttons = types.InlineKeyboardMarkup()   
    buttons.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main'))
    return buttons    