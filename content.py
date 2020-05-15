# Response to: /start
welcome_message = '''
Здравствуйте, я бот-риелтор! Чем могу помочь?
'''

# Response to: 'О нас'
about_us = '''
Telegram-bot для помощи риелторам в сборе информации от клиентов

Руководитель проекта: Тицкая Анастасия
Программист: Носова Анастасия
Аналитик: Зверева Татьяна
Тестировщик: Маркова Дарья
'''

# Response to: 'Регистрация'
introduce_yrslf = '''
Представьтесь пожалуйста...

Напишите Ф.И.О.:"
'''

user_answers = '''
Ф.И.О.:
{name}
Вид недвижимости:
{place}
Cпособ расчета:
{pay}
Важ бюджет:
{budgets}
Тип жилья:
{type_build}
Ремонт:
{remont}
Номер телефона:
{num}
'''

question = 'Все ли верно?\n' + user_answers + '\n\nОтправить?'

query_date = 'Регистрация пользователя\nUTC {current_time}'

user_data = '''
Данные пользователя (Telegram)

User: @{username}
Имя: {first_name}
Фамилия: {last_name}
ID: {id}
'''
