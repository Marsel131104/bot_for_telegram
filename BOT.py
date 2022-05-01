import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('5323541670:AAGrky6bE6J3FYQ0DmLRP8xzg6x3eHJr8G8')
k = 0


@bot.message_handler(commands=['start'])
def start(message):                                 #срабатывает при запуске бота
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    test = cursor.execute(f"""SELECT name FROM user WHERE id = {message.chat.id}""").fetchone()
    cursor.close()
    if not test:
        bot.send_message(message.chat.id, f'<b>Добро пожаловать</b>\n\nПредлагаю начать с заполнения анкеты', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'<b>Вы снова с нами 🥳🥳🥳</b>\n\nНачнем!!!',
                         parse_mode='html')
    menu(message)


@bot.message_handler(commands=['menu'])
def menu(message):                                              #освное окно бота с выбором действия
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1")                            #отвечает за то, чтобы посмотреть анкеты других пользователей из вашего города
    btn2 = types.KeyboardButton("2")                            #просмотр своей анкеты/создание своей анкеты
    btn3 = types.KeyboardButton("3")                          #отвечает за то, чтобы прекратить просмотр анкет и удалить свою анкету(другие пользователи перестанут вас видеть)
    btn4 = types.KeyboardButton("4")                            #просмотр анкет других пользователей, которые вас лайкнули
    btn5 = types.KeyboardButton("5")                            #Создание совей анкеты заново
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, f'<b>1. Смотреть анкеты.\n2. Моя анкета/создать анкету.\n3. Я больше не хочу никого искать.\n4. Посмотреть кому я понравился.\n5. Пересоздать анкету.</b>', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
  if (message.text == "1"):
    global flag
    global name_1
    flag = False
    username = message.chat.username        #переменная для проверки имени у пользователя тг (ссылка, которая нужна
                                            # для того, чтобы другие пользователи могли начать с вами диалог)
    if username == None:
        file = open('username_tg.png', 'rb')
        bot.send_photo(message.chat.id, file,
                       "Перед началом работы, пожалуйста, проверьте, что у вас есть ник, <b>как показано на фото</b>. Для того чтобы люди могли вас найти.",
                       parse_mode='html')
        start(message)
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        lol = cursor.execute(f"""SELECT name, age FROM user WHERE id == {message.chat.id}""").fetchall()  # здесь свою анкету надо показать
        if not lol:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "У вас еще не создана анкета ❌", reply_markup=markup)
            cursor.close()
            menu(message)

        else:
            #кнопки для того, чтобы лайкнуть, пропустить или прекратить просмотр анкет
            ocenivanie = types.ReplyKeyboardMarkup(resize_keyboard=True)
            like = types.KeyboardButton("♥")
            dislike = types.KeyboardButton("👎🏻")
            sleep = types.KeyboardButton("💤")
            ocenivanie.add(like, dislike, sleep)
            bot.send_message(message.chat.id, "Смотрим", reply_markup=ocenivanie)

            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cit = cursor.execute(f"""SELECT city FROM user WHERE id = {message.chat.id}""").fetchone()
            se = cursor.execute(f"""SELECT choose FROM user WHERE id = {message.chat.id}""").fetchone()
            if se[0] == 'Парни':
                sese = 'Я парень'
            else:
                sese = 'Я девушка'


            #отбор анкет по введенному городу
            viborka = cursor.execute(f"""SELECT name, age, city, photo FROM user WHERE city == ? and sex == ? and id != ?""", (cit[0], sese, message.chat.id)).fetchall()
            if viborka:
                for i in range(len(viborka)):
                    flag = False
                    name_1 = viborka[i][0]
                    age_1 = viborka[i][1]
                    city_1 = viborka[i][2]
                    photo_1 = viborka[i][3]
                    bot.send_photo(message.chat.id, photo_1, f'Нашли кое-кого для тебя 👀:\n{name_1}, {age_1}, {city_1}', reply_markup=ocenivanie)
                    bot.send_message(message.chat.id, 'Как тебе?')


                    while flag == False:        # ожидание ответа от пользователя
                        pass


                bot.send_message(message.chat.id, text="Вы просмотрели все анкеты")
                menu(message)
            else:
                bot.send_message(message.chat.id, "К сожалению, мы пока не можем никого вам найти 😢")
                menu(message)


  elif (message.text == "2"):
    ocenivanie = types.ReplyKeyboardRemove(selective=False)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    lol = cursor.execute(f"""SELECT name, age FROM user WHERE id = {message.chat.id}""").fetchall()  # здесь свою анкету надо показать
    if not lol:
        username = message.chat.username
        if username == None:
            file = open('username_tg.png', 'rb')
            bot.send_photo(message.chat.id, file,
                           "Перед началом работы, пожалуйста, проверьте, что у вас есть ник, <b>как показано на фото</b>. Для того чтобы люди могли вас найти.",
                           parse_mode='html')
            start(message)
        else:
            bot.send_message(message.chat.id, "Начнем создавать анкету 👾", reply_markup=ocenivanie)
            cursor.close()
            reg(message)
    else:
        nam = cursor.execute(f"""SELECT name FROM user WHERE id = {message.chat.id}""").fetchone()
        ag = cursor.execute(f"""SELECT age FROM user WHERE id = {message.chat.id}""").fetchone()
        phot = cursor.execute(f"""SELECT photo FROM user WHERE id = {message.chat.id}""").fetchone()
        sob = cursor.execute(f"""SELECT nik FROM user WHERE id = {message.chat.id}""").fetchone()
        bot.send_photo(message.chat.id, phot[0], f'Ваша анкета:\n{nam[0]}, {ag[0]}, {sob[0]}')
        cursor.close()
        menu(message)

  elif (message.text == "3"):
    global mark
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton("Да, уверен ☺")
    btn_no = types.KeyboardButton("Нет, вернуться назад ♻")
    mark.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, "Ты уверен?", reply_markup=mark)

  elif (message.text == 'Да, уверен ☺'):                        #удаление анкеты
    mark = types.ReplyKeyboardRemove(selective=False)
    back = types.ReplyKeyboardMarkup(resize_keyboard=True)
    behind = types.KeyboardButton("Вернуться назад ♻")          #возвращаемся в меню
    back.add(behind)
    bot.send_message(message.chat.id, "🆗", reply_markup=back)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"""DELETE FROM user WHERE id = {message.chat.id}""")
    connect.commit()
    cursor.close()


  elif message.text == '4':                 #просмотр анкет других пользователей, которые вас лайкнули
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    try:
        mn = cursor.execute(f"""SELECT name FROM user WHERE id = {message.chat.id}""").fetchone()[0]
        list_of_liking = cursor.execute("""SELECT my_name, my_age, my_city, my_nik, my_photo FROM liking WHERE your_name = ?""", (mn,)).fetchall()
        if not list_of_liking:
            bot.send_message(message.chat.id, "<strong>Вас пока никто не лайкнул 🥱</strong>", parse_mode='html')        #если никто не вас не лайкнул
            menu(message)
        else:
           for i in range(len(list_of_liking)):
               name_liking = list_of_liking[i][0]
               age_liking = list_of_liking[i][1]
               city_liking = list_of_liking[i][2]
               nik_liking = list_of_liking[i][3]
               photo_liking = list_of_liking[i][4]
               bot.send_photo(message.chat.id, photo_liking, f'Вами кто-то заинтересовался 🤔:\n{name_liking}, {age_liking}, {city_liking}\n\n<b>Хорошо вам провести время: </b>{nik_liking}', parse_mode='html')
           cursor.execute("""DELETE FROM liking WHERE your_name = ?""", (mn,))
           connect.commit()
           cursor.close()
           menu(message)
    except Exception:
        bot.send_message(message.chat.id, "У вас еще не создана анкета ❌")
        cursor.close()
        menu(message)

  elif message.text == '5':
      markup = types.ReplyKeyboardRemove(selective=False)
      connect = sqlite3.connect('users.db')
      cursor = connect.cursor()
      test = cursor.execute(f"""SELECT name FROM user WHERE id = {message.chat.id}""").fetchone()
      if not test:
          bot.send_message(message.chat.id, "Перед тем как изменять анкету создайте ее 😡")
          menu(message)
      else:
          cursor.execute(f"""DELETE FROM user WHERE id = {message.chat.id}""")
          connect.commit()
          cursor.close()
          bot.send_message(message.chat.id, "Вас понял, выполняю 🤖", reply_markup=markup)
          reg(message)



    #кнопки, которые возращают нас в меню
  elif (message.text == 'Нет, вернуться назад ♻' or message.text == '💤' or message.text == 'Меню' or message.text == 'Вернуться назад ♻'):
    menu(message)


  elif message.text == '♥':                     #лайк пользователю
      connect = sqlite3.connect('users.db')
      cursor = connect.cursor()

      my_name = cursor.execute(f"""SELECT name FROM user WHERE id = {message.chat.id}""").fetchone()
      my_age = cursor.execute(f"""SELECT age FROM user WHERE id = {message.chat.id}""").fetchone()
      my_city = cursor.execute(f"""SELECT city FROM user WHERE id = {message.chat.id}""").fetchone()
      my_nik = cursor.execute(f"""SELECT nik FROM user WHERE id = {message.chat.id}""").fetchone()
      my_photo = cursor.execute(f"""SELECT photo FROM user WHERE id = {message.chat.id}""").fetchone()
      al = cursor.execute(f"""SELECT * FROM liking""").fetchall()
      your_name = name_1
      jj = 0
      for i in range(len(al)):
          if my_name[0] in al[i] and your_name in al[i]:
              jj += 1
      if jj == 0:                           #более одного раза одного и того же пользователя лайкнуть нельзя
          cursor.execute("""INSERT INTO liking VALUES(?, ?, ?, ?, ?, ?)""",
                         (my_name[0], my_age[0], my_city[0], my_nik[0], my_photo[0], your_name))
          connect.commit()
          cursor.close()
      else:
          pass

      flag = True



  elif message.text == '👎🏻':        #если нам не понравилась анкета, то пропускаем ее
      flag = True



def reg(message):           #начало создания своей анкеты
    global l
    l = {}
    vr = []
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    spis = cursor.execute("""SELECT id FROM user""").fetchall()
    for i in spis:
        vr.append(*i)
    if  message.chat.id in vr:
        cursor.execute(f"""DELETE FROM user WHERE id == {message.chat.id}""")
        connect.commit()
        cursor.close()
        msg = bot.send_message(message.chat.id, "Как тебя зовут?")
        bot.register_next_step_handler(msg, name)
    else:
        msg = bot.send_message(message.chat.id, "Как тебя зовут?")
        bot.register_next_step_handler(msg, name)
        cursor.close()


def name(message):                          #получаем имя, оно будет использоваться везде при обращении бота к нам
    if message.text == None:
        msg = bot.reply_to(message, 'Еще раз, как тебя зовут?')
        bot.register_next_step_handler(msg, name)
    else:
        l['name'] = message.text
        msg = bot.send_message(message.chat.id, "Сколько тебе лет?")
        bot.register_next_step_handler(msg, age)


def age(message):                   #получаем введенный возраст
    try:
        int(message.text)
        l['age'] = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('Я парень')
        btn2 = types.KeyboardButton('Я девушка')
        markup.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, "Теперь определимся с полом", reply_markup=markup)
        bot.register_next_step_handler(msg, sex)
    except Exception:
        msg = bot.reply_to(message, 'oops...Неверный формат')
        bot.register_next_step_handler(msg, age)



def sex(message):                               #получаем пол пользователя
    if message.text == 'Я парень' or message.text == 'Я девушка':
        l['sex'] = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('Парни')
        btn2 = types.KeyboardButton('Девушки')
        markup.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, "Кто тебе интересен?", reply_markup=markup)
        bot.register_next_step_handler(msg, choose)
    else:
        msg = bot.reply_to(message, 'Еще раз, определимся с полом\n\nНАЖМИ НА ЛЮБУЮ ИЗ ДАННЫХ КНОПОК')
        bot.register_next_step_handler(msg, sex)


def choose(message):                            #предпочтение пользователя к поиску других людей по полу
    if message.text == 'Парни' or message.text == 'Девушки':
        markup = types.ReplyKeyboardRemove(selective=False)
        l['choose'] = message.text
        msg = bot.send_message(message.chat.id, "Из какого ты города?", reply_markup=markup)
        bot.register_next_step_handler(msg, city)
    else:
        msg = bot.reply_to(message, 'Кто тебе интересен?\n\nНАЖМИ НА ЛЮБУЮ ИЗ ДАННЫХ КНОПОК')
        bot.register_next_step_handler(msg, choose)


def city(message):                              #получаем город пользователя
    if message.text == None:
        msg = bot.reply_to(message, 'Вы отправили что-то другое, попробуем еще раз...\nИз какого вы города?')
        bot.register_next_step_handler(msg, city)
    else:
        a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        flag = True
        for i in range(len(message.text)):
            if message.text[i] not in a:
                continue
            else:
                flag = False

        if flag:
            l['city'] = message.text
            msg = bot.send_message(message.chat.id, "Теперь пришли свое фото, его будут видеть другие пользователи")
            bot.register_next_step_handler(msg, photo)
        else:
            msg = bot.reply_to(message, 'Хм.. Кажется такого города не существует\nИз какого вы города?')
            bot.register_next_step_handler(msg, city)


def photo(message):                 #получаем фото пользователя
    if message.photo == None:               #проверка на отправку именно фото
        msg = bot.reply_to(message, 'Отправьте пожалуйста фото')
        bot.register_next_step_handler(msg, photo)
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                       (message.chat.id, l['name'], l['age'], l['sex'], l['choose'], l['city'],
                        message.photo[0].file_id, '@' + message.chat.username))
        connect.commit()

        nam = cursor.execute(f"""SELECT name FROM user WHERE id = {message.chat.id}""").fetchone()
        ag = cursor.execute(f"""SELECT age FROM user WHERE id = {message.chat.id}""").fetchone()
        phot = cursor.execute(f"""SELECT photo FROM user WHERE id = {message.chat.id}""").fetchone()
        sob = cursor.execute(f"""SELECT nik FROM user WHERE id = {message.chat.id}""").fetchone()

        bot.send_photo(message.chat.id, phot[0], f'Ваша анкета создана ✅:\n{nam[0]}, {ag[0]}, {sob[0]}')
        cursor.close()
        menu(message)


bot.polling(none_stop=True)