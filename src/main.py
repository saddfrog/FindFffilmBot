from functions_for_bot import *

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 
                     "Привет)\nБот предназначен для подбора фильма по категориям", reply_markup=main_b())
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.from_user.id, "Что бы начать работу с ботом введите команду /start")

@bot.message_handler(content_types=['sticker'])
def start_message(message):
        bot.send_message(message.from_user.id, "Забавный стикер 😁")
@bot.message_handler()
def start_message(message):
        bot.send_message(message.from_user.id, "К сожалению, я не умею читать, но я уверен, что там что-то хорошее😜")

@bot.callback_query_handler(func=lambda call: True)    
def call_back(call):
    del_prev_buttons(call)
    if "_page_" in call.data:
            parts = call.data.split("_page_")
            type_selection = parts[0]
            page = int(parts[1])
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=selection_b(type_selection, page)
            )
            return
    if call.data == 'main':
        # del_prev_buttons(call)
        bot.send_message(chat_id=call.message.chat.id, text="тестим кнопки\n"
       "Выберите, каким способом подобрать фильм", reply_markup=main_b())      
    if call.data == 'selection_menu':
        # del_prev_buttons(call)
        bot.send_message(chat_id=call.message.chat.id, text="Вот текущие подборки:",reply_markup=selection_menu_b())
    if call.data in ['sel_genre', 'sel_actor', 'sel_year', 'sel_all_actor', 'sel_all_films']:
        setting = call.data 
        bot.send_message(chat_id=call.message.chat.id, text="Выбор подборки фильма",reply_markup=selection_b(setting))
    if call.data in callback_map:
        real_value = callback_map[call.data]
        bot.send_message(call.message.chat.id, f"Ты выбрал: {real_value}")

    if call.data == 'random_film':   
        film = random_film() 
        # del_prev_buttons(call)
        bot.send_photo(chat_id=call.message.chat.id,photo=film[6] ,caption=f"🎬*Ваш фильм*: `{film[1]}`\n\n*Описание фильма*: {film[7]}\n\n *Возрастной рейтинг*: {film[15]}",parse_mode="MARKDOWN", reply_markup=random_film_b())
    if call.data == 'user_choose':   
        # del_prev_buttons(call)
        bot.send_message(chat_id=call.message.chat.id, text=f"🫣Пока в разработке...", reply_markup=user_choose_b())

bot.polling(none_stop=True, interval=0)