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
    
    if call.data == 'main':
        # del_prev_buttons(call)
        bot.send_message(chat_id=call.message.chat.id, text="тестим кнопки\n"
       "Выберите, каким способом подобрать фильм", reply_markup=main_b())      

    if call.data in callback_map:
        real_value = callback_map[call.data]
        bot.send_message(call.message.chat.id, f"Ты выбрал: {real_value}")

    if call.data == 'random_film':   
        film = random_film() 
        # del_prev_buttons(call)
        bot.send_photo(chat_id=call.message.chat.id,photo=film[6] ,caption=f"🎬*Ваш фильм*: `{film[1]}`\n\n*Описание фильма*: {film[7]}\n\n *Возрастной рейтинг*: {film[15]}",parse_mode="MARKDOWN", reply_markup=random_film_b())
   
    if call.data == 'user_choose':
        user_filters[call.message.chat.id] = {}  # сброс
        bot.send_message(call.message.chat.id, "Выберите фильтр:", reply_markup=filter_menu_b())

    if call.data == 'reset_filters':
        user_filters[call.message.chat.id] = {}  # очищаем все фильтры
        print(user_filters[call.message.chat.id])

        bot.send_message(text="🧹 Все фильтры сброшены.",chat_id=call.message.chat.id, reply_markup=filter_menu_b())

    if call.data == 'choose_year':
        markup = types.InlineKeyboardMarkup()
        decades = {
            '1980': '1980–1989',
            '1990': '1990–1999',
            '2000': '2000–2009',
            '2010': '2010–2019',
            '2020': '2020–2029'
        }
        for key, label in decades.items():
            markup.add(types.InlineKeyboardButton(label, callback_data=f'set_year_{key}'))
        bot.send_message(call.message.chat.id, "Выберите десятилетие выпуска:", reply_markup=markup)

    if call.data == 'choose_genre':
        markup = types.InlineKeyboardMarkup()
        for i in range(0, len(genre), 3):
            buttons = []
            for j in range(3):
                if i + j < len(genre):
                    buttons.append(types.InlineKeyboardButton(genre[i + j], callback_data=f'set_genre_{genre[i + j]}'))            
            markup.add(*buttons)
        markup.add(types.InlineKeyboardButton("ничего", callback_data=f'set_genre_none'))

        bot.send_message(call.message.chat.id, "Выберите страну:", reply_markup=markup)

    if call.data == 'choose_country':
        markup = types.InlineKeyboardMarkup()
        for i in range(0, len(countries), 3):
            buttons = []
            for j in range(3):
                if i + j < len(countries):
                    buttons.append(types.InlineKeyboardButton(countries[i + j], callback_data=f'set_country_{countries[i + j]}'))            
            markup.add(*buttons)
        markup.add(types.InlineKeyboardButton("ничего", callback_data=f'set_country_none'))

        bot.send_message(call.message.chat.id, "Выберите страну:", reply_markup=markup)

    if call.data == 'choose_age':
        markup = types.InlineKeyboardMarkup()
        for age in ages:
            markup.add(types.InlineKeyboardButton(age, callback_data=f'set_age_{age}'))
        bot.send_message(call.message.chat.id, "Выберите возрастной рейтинг:", reply_markup=markup)

    if call.data == 'choose_actor':
        markup = types.InlineKeyboardMarkup()
        for i in range(0, len(actors), 3):
            buttons = []
            for j in range(3):
                if i + j < len(actors):
                    buttons.append(types.InlineKeyboardButton(actors[i + j], callback_data=f'set_actor_{actors[i + j]}'))            
            markup.add(*buttons)
        markup.add(types.InlineKeyboardButton("ничего", callback_data=f'set_actor_none'))

        bot.send_message(call.message.chat.id, "Выберите актёра:", reply_markup=markup)
        
    if call.data.startswith('set_year_'):
        year = call.data.split('_')[-1]
        user_filters.setdefault(call.message.chat.id, {})['year'] = year
        summary = format_filter_summary(user_filters[call.message.chat.id])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, f"✅ Год выбран.\n\n{summary}", parse_mode='Markdown', reply_markup=filter_menu_b())

    if call.data.startswith('set_genre_'):
        g = call.data.split('_', 2)[2]
        if g == 'none':
            user_filters[call.message.chat.id].pop('genre', None)
            g = 'не'
        else:
            user_filters.setdefault(call.message.chat.id, {})['genre'] = g
        summary = format_filter_summary(user_filters[call.message.chat.id])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, f"✅ Жанр: {g} выбран.\n\n{summary}", parse_mode='Markdown', reply_markup=filter_menu_b())

    if call.data.startswith('set_country_'):
        c = call.data.split('_', 2)[2]
        if c == 'none':
            user_filters[call.message.chat.id].pop('country', None)
            c = 'не'
        else:
            user_filters.setdefault(call.message.chat.id, {})['country'] = c
        summary = format_filter_summary(user_filters[call.message.chat.id]) 
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) 

        bot.send_message(call.message.chat.id, f"✅ Страна: {c} выбрана.\n\n{summary}",parse_mode='Markdown', reply_markup=filter_menu_b())
        print(user_filters[call.message.chat.id])

    if call.data.startswith('set_age_'):
        a = call.data.split('_')[-1]
        user_filters.setdefault(call.message.chat.id, {})['age'] = a
        summary = format_filter_summary(user_filters[call.message.chat.id])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, f"✅ Возрастной рейтинг: {a} выбран.\n\n{summary}",parse_mode='Markdown', reply_markup=filter_menu_b())

    if call.data.startswith('set_actor_'):
        a = call.data.split('_', 2)[2]
        if a == 'none':
            user_filters[call.message.chat.id].pop('actor', None)
            a = 'не'
        else:
            user_filters.setdefault(call.message.chat.id, {})['actor'] = a
        summary = format_filter_summary(user_filters[call.message.chat.id])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, f"✅ Актёр: {a} выбран.\n\n{summary}",parse_mode='Markdown', reply_markup=filter_menu_b())

    if call.data == 'show_filtered':
        filters = user_filters.get(call.message.chat.id, {})
        results = []

        with open('src/kinopoisk_top250_full.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'year' in filters:
                    start = int(filters['year'])
                    end = start + 9
                    if not (start <= int(row['year']) <= end):
                        continue

                if 'genre' in filters and filters['genre'] not in row['genres']:
                    continue
                if 'country' in filters and filters['country'] not in row['countries']:
                    continue
                if 'age' in filters and filters['age'] not in row['age_rating']:
                    continue
                if 'actor' in filters and filters['actor'] not in row['actors']:
                    continue
                results.append(row)
        if not results:
            bot.send_message(call.message.chat.id, "Ничего не найдено по заданным фильтрам 😢", reply_markup=filter_menu_b())
        else:
            filtred_films(call.message.chat.id, results)

bot.polling(none_stop=True, interval=0)