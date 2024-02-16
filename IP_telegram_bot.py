import telebot
from telebot import types

bot = telebot.TeleBot('5946052011:AAEPKT8-_6MwvMn7uAjwt13d_SYhFgQ-sBc')
name = ''
surname = ''
age = 0
info_arr = []
tmp = ''
tmp2 = ''
flag = True


@bot.message_handler(commands=['info'])
def info(message):
    f = open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8').readlines()
    for el in f:
        el = el.split(' ')
        bot.send_message(message.from_user.id,
                         'Имя:' + ' ' + el[0] + '\n' + 'Фамилия:' + ' ' + el[1] + '\n' + 'Возраст:' + ' ' + el[2])


@bot.message_handler(commands=['fix'])
def fix(message):
    bot.send_message(message.from_user.id, 'С чем вы хотите взаимодействовать (напишите фамилию или имя)')
    bot.register_next_step_handler(message, get_user_info)


def get_user_info(message):
    global tmp
    tmp = message.text
    f = open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8').readlines()
    for el in f:
        el = el.split(' ')
        if el[0] == message.text:
            bot.send_message(message.from_user.id, 'Что вы хотите изменить - фамилию, имя')
            bot.register_next_step_handler(message, change_user_info)
            return True
        elif el[1] == message.text:
            bot.send_message(message.from_user.id, 'Что вы хотите изменить - фамилию или имя')
            bot.register_next_step_handler(message, change_user_info)
            return True
    bot.send_message(message.from_user.id, 'Такая фамилия или такое имя отсутствует в списке!')


def change_user_info(message):
    if message.text.lower() == "имя":
        bot.send_message(message.from_user.id, 'Введите новое имя')
        bot.register_next_step_handler(message, change_user_name)
    elif message.text.lower() == 'фамилию' or message.text.lower() == 'фамилия':
        bot.send_message(message.from_user.id, 'Введите новую фамилию')
        bot.register_next_step_handler(message, change_user_surname)
    # elif message.text.lower() == 'возраст':
    #     bot.send_message(message.from_user.id, 'Введите новый возраст')
    #     bot.register_next_step_handler(message, change_user_age)


@bot.message_handler(commands=['delete'])
def delete_name(message):
    bot.send_message(message.from_user.id, 'Введите имя того, кого хотите удалить: ')
    bot.register_next_step_handler(message, delete_surname)


def delete_surname(message):
    global tmp
    bot.send_message(message.from_user.id, 'Введите фамилию: ')
    tmp = message.text
    bot.register_next_step_handler(message, delete_age)


def delete_age(message):
    global tmp2
    bot.send_message(message.from_user.id, 'Введите возраст: ')
    tmp2 = message.text
    bot.register_next_step_handler(message, delete_all)


def delete_all(message):
    global tmp
    global tmp2
    new_data2 = ''
    with open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8') as f:
        old_data = f.read()
    if tmp not in old_data or tmp2 not in old_data or message.text not in old_data:
        bot.send_message(message.from_user.id, 'Такого пользователя не существует, вот все пользователи: ')
        info(message)
    else:
        new_data = old_data.replace(tmp, '', 1)
        new_data = new_data.replace(tmp2, '', 1)
        new_data = new_data.replace(message.text, '', 1)
        for el in new_data.split('\n'):
            new_el = el.split(' ')
            if new_el[0] != '' and new_el[1] != '' and new_el[2] != '':
                new_data2 += el
                new_data2 += '\n'
        with open(str(message.chat.id) + '.txt', 'w', encoding='UTF-8') as f:
            f.write(new_data2)
        bot.send_message(message.from_user.id, 'Пользователь удалён!')


def change_user_name(message):
    global tmp
    with open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8') as f:
        old_data = f.read()
    new_data = old_data.replace(tmp, message.text, 1)
    with open(str(message.chat.id) + '.txt', 'w', encoding='UTF-8') as f:
        f.write(new_data)
    bot.send_message(message.from_user.id, 'Имя изменено!')


def change_user_surname(message):
    global tmp
    with open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8') as f:
        old_data = f.read()
    new_data = old_data.replace(tmp, message.text, 1)
    with open(str(message.chat.id) + '.txt', 'w') as f:
        f.write(new_data)
    bot.send_message(message.from_user.id, 'Фамилия изменена!')


def change_user_age(message):
    global tmp
    with open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8') as f:
        old_data = f.read()
    new_data = old_data.replace(tmp, message.text, 1)
    with open(str(message.chat.id) + '.txt', 'w', encoding='UTF-8') as f:
        f.write(new_data)
    bot.send_message(message.from_user.id, 'Фамилия изменена!')


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    age = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + surname + ' ' + name + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        f = open(str(call.message.chat.id) + '.txt', 'a', encoding='UTF-8')
        f.write(name + ' ' + surname + ' ' + str(age) + '\n')
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Напиши функицю /reg для нового заполнения данных')


@bot.message_handler(content_types=['text'])
def start(message):
    global flag
    if flag:
        f = open(str(message.chat.id) + '.txt', 'a', encoding='UTF-8')
        flag = False
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


bot.polling(none_stop=True)
