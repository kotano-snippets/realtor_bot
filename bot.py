###################################################################################
from telebot import types
import telebot
import time
import config
###################################################################################
bot = telebot.TeleBot(config.token)
###################################################################################
mainkeyboard = types.ReplyKeyboardMarkup(row_width=2)
mainkeyboard.row("О нас")
mainkeyboard.row("Регистрация")

rus_num = types.ReplyKeyboardMarkup(row_width=2)
rus_num.row("Да")
rus_num.row("Нет")

cancel = types.ReplyKeyboardMarkup(row_width=2)
cancel.add("Не важно")
cancel.add("Отменить")

cancel1 = types.ReplyKeyboardMarkup(row_width=2)
cancel1.add("Отменить")

place_keyboard = types.ReplyKeyboardMarkup(row_width=2)
place_keyboard.row("Квартира")
place_keyboard.row("Загородный дом")
place_keyboard.add("Не важно")
place_keyboard.add("Отменить")

pay_keyboard = types.ReplyKeyboardMarkup(row_width=2)
pay_keyboard.row("Ипотека")
pay_keyboard.row("Наличные")
pay_keyboard.add("Не важно")
pay_keyboard.row("Отменить")

type_build_keyboard = types.ReplyKeyboardMarkup(row_width=2)
type_build_keyboard.row("Вторичное")
type_build_keyboard.row("Новое")
type_build_keyboard.add("Не важно")
type_build_keyboard.row("Отменить")

remont_keyboard = types.ReplyKeyboardMarkup(row_width=2)
remont_keyboard.row("Требует ремонта", "Косметический")
remont_keyboard.row("По дизайну проекта", "Современный")
remont_keyboard.add("Не важно")
remont_keyboard.row("Отменить")
###################################################################################
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Здраствуйте я телеграмм бот", reply_markup=mainkeyboard)
###################################################################################
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	if message.text == "О нас":
		bot.send_message(message.chat.id, "Telegram-bot для помощи риелторам в сборе информации от клиентов\
                                            \n\nРуководитель проекта: Тицкая Анастасия\
                                            \nПрограммист: Носова Анастасия\
                                            \nАналитик: Зверева Татьяна\
                                            \nТестировщик: Маркова Дарья")
	elif message.text == "Регистрация":
		bot.send_message(message.from_user.id, "Представьтесь пожалуйста...\n\nНапишите Ф.И.О.:", reply_markup=cancel)
		bot.register_next_step_handler(message, get_name)
	elif message.text == "Отменить":
	    bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
###################################################################################
def get_name(message):
    global name
    name = message.text
    if name == "Отменить" or name == "отменить":
    	bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
    	pass
    else:
    	bot.send_message(message.chat.id, 'Выберите вид недвижимости:', reply_markup=place_keyboard)
    	bot.register_next_step_handler(message, get_place)

def get_place(message):
    global place
    place = message.text
    if place == "Отменить" or place == "отменить":
    	bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
    	pass
    else:
    	bot.send_message(message.chat.id, 'Выберите способ расчета:', reply_markup=pay_keyboard)
    	bot.register_next_step_handler(message, get_pay)

def get_pay(message):
	global pay
	pay = message.text
	if pay == "Отменить" or pay == "отменить":
		bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
		pass
	else:
		bot.send_message(message.chat.id, 'Введите максимальный бюджет:', reply_markup=cancel)
		bot.register_next_step_handler(message, get_budgets)

def get_budgets(message):
	global budgets
	budgets = message.text
	if budgets == "Отменить" or budgets == "отменить":
		bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
		pass
	else:
		bot.send_message(message.chat.id, "Тип жилья", reply_markup=type_build_keyboard)
		bot.register_next_step_handler(message, get_type_build)

def get_type_build(message):
	global type_build
	type_build = message.text
	if type_build == "Отменить" or type_build == "отменить":
		bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
		pass
	else:
		bot.send_message(message.chat.id, "Выберите ремонт:", reply_markup=remont_keyboard)
		bot.register_next_step_handler(message, get_remont)

def get_remont(message):
	global remont
	remont = message.text
	if remont == "Отменить" or remont == "отменить":
		bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
		pass
	else:
		bot.send_message(message.chat.id, "Укажите свой номер телефона:", reply_markup=cancel1)
		bot.register_next_step_handler(message, get_num)

def get_num(message):
	global num
	global results
	num = message.text
	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text="Да", callback_data='yes')
	keyboard.add(key_yes)
	key_no = types.InlineKeyboardButton(text="Нет", callback_data='no')
	keyboard.add(key_no)
	question = "Все ли верно?" + "\n`Ф.И.О.:`\n" + name + "\n`Вид недвижимости:`\n" + place + "\n`Cпособ расчета:`\n" + pay + "\n`Важ бюджет:`\n" + budgets + "\n`Тип жилья:`\n" + type_build + "\n`Ремонт:`\n" + remont + "\n`Номер телефона:`\n" + num + "\n\n\n" + "Отправить ?"
	if num == "Отменить" or num == "отменить":
		bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=mainkeyboard)
		pass
	else:
		results = bot.send_message(message.chat.id, text=question, reply_markup=keyboard, parse_mode="markdown")
###################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
    	if call.data == "yes":
    	    admin = config.admin
    	    bot.send_message(admin, 'Регистрация пользователя\nUTC ' + str(time.ctime()) + "\n" + "\n`Ф.И.О.:`\n" + name + "\n`Вид недвижимости:`\n" + place + "\n`Cпособ расчета:`\n" + pay + "\n`Важ бюджет:`\n" + budgets + "\n`Тип жилья:`\n" + type_build + "\n`Ремонт:`\n" + remont + "\n`Номер телефона:`\n" + num + "\n\nДанные пользователя (Telegram)\
    	                                                                                                                                                                                                                                                                                                                     \nUser: @{0}\
                                                                                                                                                                                                                                                                                                                             \nИмя: {1}\
                                                                                                                                                                                                                                                                                                                             \nФамилия: {2}\
                                                                                                                                                                                                                                                                                                                             \nID: {3}".format(call.from_user.username, call.from_user.first_name,
                                                                                                                                                                                                                                                                                                                                                       call.from_user.last_name,
                                                                                                                                                                                                                                                                                                                                                       str(call.from_user.id)), parse_mode="markdown")
    	    bot.delete_message(call.message.chat.id, results.message_id)
    	    bot.send_message(call.message.chat.id, "Сообщение отправлено!)\nЖдите ответа от Администратора", reply_markup=mainkeyboard)
    	elif call.data == 'no':
    	    bot.delete_message(call.message.chat.id, results.message_id)
    	    bot.send_message(call.message.chat.id, "Отправка отменена", reply_markup=mainkeyboard)
    except:
        bot.send_message(call.message.chat.id, "Перезагрузите бота \n/start")
###################################################################################
if __name__ == '__main__':
	bot.polling(none_stop=True)
###################################################################################
