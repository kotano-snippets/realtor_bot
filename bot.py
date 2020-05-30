from time import ctime

import telebot
from requests.exceptions import (
    ConnectTimeout, ProxyError, ReadTimeout)
from telebot import apihelper, types

import config
import content as c

bot = telebot.TeleBot(config.token)

answers = {}


def make_keyboard(replies, width=1, cancel=True, extra=''):
    '''Add reply keyboard

        Parameters:
            replies(list): list of replies
            width(int): max width of rows
            cancel(bool): set to False if you don't want cancel btn to appear
    '''
    keyb = types.ReplyKeyboardMarkup(row_width=width)
    keyb.add(*replies)
    if extra:
        keyb.row(extra)
    if cancel:
        keyb.row('Отменить')
    return keyb


# Keyboards
K_MAIN = make_keyboard(['О нас', 'Регистрация'], 1, False, None)
K_CANCEL = make_keyboard([], extra='Не важно')
K_YESNO = make_keyboard(["Да", "Нет"], 2, False, None)


def check_cancel(func):
    '''Decorator;
    If answered 'отменить' get back to
    mainkeyboard and return message object'''

    def inner(message):
        if message.text.lower() == "отменить":
            bot.send_message(
                message.chat.id, "Вы вернулись назад",
                reply_markup=K_MAIN)
            return message
        else:
            return func(message)
    return inner


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.from_user.id)
    return bot.send_message(
        message.chat.id, c.welcome_message, reply_markup=K_MAIN)


@bot.message_handler(content_types=["text"])
@check_cancel
def repeat_all_messages(message):
    if message.text == "О нас":
        bot.send_message(message.chat.id, c.about_us)
    elif message.text == "Регистрация":
        bot.send_message(
            message.from_user.id, c.introduce_yrslf, reply_markup=K_CANCEL)
        bot.register_next_step_handler(message, get_name)


@check_cancel
def get_name(message):
    name = message.text
    answers['name'] = name
    place_keyboard = make_keyboard(
        ["Квартира", "Загородный дом"], width=2, extra="Не важно")
    bot.send_message(
        message.chat.id, 'Выберите вид недвижимости:',
        reply_markup=place_keyboard)
    bot.register_next_step_handler(message, get_place)


@check_cancel
def get_place(message):
    place = message.text
    answers['place'] = place
    pay_keyboard = make_keyboard(
        ["Ипотека", "Наличные"], width=2, extra="Не важно")
    bot.send_message(
        message.chat.id, 'Выберите способ расчета:',
        reply_markup=pay_keyboard)
    bot.register_next_step_handler(message, get_pay)


@check_cancel
def get_pay(message):
    pay = message.text
    answers['pay'] = pay
    bot.send_message(
        message.chat.id, 'Введите максимальный бюджет:',
        reply_markup=K_CANCEL)
    bot.register_next_step_handler(message, get_budgets)


@check_cancel
def get_budgets(message):
    budgets = message.text
    answers['budgets'] = budgets
    type_build_keyboard = make_keyboard(
        ["Вторичное", "Новое"], width=2, extra="Не важно")
    bot.send_message(message.chat.id, "Тип жилья",
                     reply_markup=type_build_keyboard)
    bot.register_next_step_handler(message, get_type_build)


@check_cancel
def get_type_build(message):
    type_build = message.text
    answers['type_build'] = type_build
    remont_keyboard = make_keyboard(
        ["Требует ремонта", "Косметический",
         "По дизайну проекта", "Современный"],
        width=2, extra="Не важно")
    bot.send_message(message.chat.id, "Выберите ремонт:",
                     reply_markup=remont_keyboard)
    bot.register_next_step_handler(message, get_remont)


@check_cancel
def get_remont(message):
    remont = message.text
    answers['remont'] = remont
    bot.send_message(
        message.chat.id, "Укажите свой номер телефона:",
        reply_markup=make_keyboard([]))
    bot.register_next_step_handler(message, get_num)


@check_cancel
def get_num(message):
    global results
    num = message.text
    answers['num'] = num
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да", callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет", callback_data='no')
    keyboard.add(key_no)
    question = c.question.format(**answers)

    results = bot.send_message(
        message.chat.id, text=question,
        reply_markup=keyboard, parse_mode="markdown")
    return results


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data == "yes":
            admin = config.admin
            user_data = c.user_data.format(
                username=call.from_user.username,
                first_name=call.from_user.first_name,
                last_name=call.from_user.last_name,
                id=call.from_user.id)
            r = bot.send_message(
                admin,
                text=(
                    c.query_date.format(current_time=ctime()) +
                    c.user_answers.format(**answers) +
                    user_data))

            bot.delete_message(call.message.chat.id, results.message_id)
            bot.send_message(
                call.message.chat.id,
                "Сообщение отправлено!)\nЖдите ответа от Администратора",
                reply_markup=K_MAIN)
            return r
        elif call.data == 'no':
            bot.delete_message(call.message.chat.id, results.message_id)
            bot.send_message(
                call.message.chat.id, "Отправка отменена",
                reply_markup=K_MAIN)
    except Exception as e:
        print(e)
        bot.send_message(call.message.chat.id, "Перезагрузите бота \n/start")


def start_bot(bot):
    '''Start bot. If can't connect, use proxy if allow_proxy == True'''
    try:
        bot.polling(none_stop=True)
    except (ReadTimeout, ConnectTimeout, ProxyError):
        if config.allow_proxy:
            apihelper.proxy = {'https': next(config.proxies)}
            print('Change proxy to: ', apihelper.proxy)
            start_bot(bot)


if __name__ == '__main__':
    print('\n\n\nStart\n\n\n')
    start_bot(bot)
