from functions_for_bot import *
# import math

# bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 
                     "Привет)\nБот предназначен для подбора фильма по категориям", reply_markup=main_b())
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.from_user.id, "Что бы начать работу с ботом введите команду /start")

@bot.callback_query_handler(func=lambda call: True)    
def call_back(call):
    if call.data == 'main':
        bot.send_message(chat_id=call.message.chat.id, text="тестим кнопки\n"
       "Выберите, каким способом подобрать фильм", reply_markup=main_b())       
    if call.data == 'random_film':   
        film = random_film() 
        bot.send_message(chat_id=call.message.chat.id, text=f"Ваш фильм: {film}", reply_markup=random_film_b())
    if call.data == 'user_choose':   
        bot.send_message(chat_id=call.message.chat.id, text=f"Пока в разработке...", reply_markup=user_choose_b())

  

bot.polling(none_stop=True, interval=0)