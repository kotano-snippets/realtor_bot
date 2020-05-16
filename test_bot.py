import pytest

import config
import content as c
import bot as b
from bot import time


# NOTE: Test time may vary depending on connection speed
# and server availability.

testbot_username = '@kotpybot'
test_token = '821235624:AAFlR4yJHGaEYP725DRXBFHKqwV6uxA-DB0'
test_id = 905484789

test_answers = {
    'name': 'testman', 'place': 'program', 'pay': 'Cash',
    'budgets': '100', 'type_build': 'New',
    'remont': 'remonted)', 'num': '6811500121'
}

# test_user_data
tud = {
    'username': 'bot_tester', 'first_name': 'tester',
    'last_name': 'None', 'id': test_id
}


class Dct(dict):
    pass


class Message(Dct):
    def __init__(self, text):
        self.text = text
        self.chat = Dct()
        self.from_user = Dct()
        self.chat.id = test_id
        self.from_user.id = test_id


class Call(Dct):
    def __init__(self, data):
        self.data = data
        self.from_user = Dct()
        self.from_user.username = tud['username']
        self.from_user.first_name = tud['first_name']
        self.from_user.last_name = tud['last_name']
        self.from_user.id = tud['id']
        self.message = Message('Да')


# TODO: Figure out how to reduce connection time
@pytest.fixture
def return_bot():
    bot = b.telebot.TeleBot(test_token)
    b.start_bot(bot)
    return bot


@pytest.fixture
def test_data(monkeypatch):
    '''Patch input data and return tuple(id, answers)'''
    monkeypatch.setattr(config, 'admin', test_id)
    monkeypatch.setattr(b, 'answers', test_answers)
    return test_id, test_answers


# @pytest.mark.skip
def test_start(monkeypatch, test_data):
    message = Message('/start')
    r = b.start_message(message)
    assert r.text == c.welcome_message.strip()


def test_get_num(monkeypatch):
    message = Message(test_answers['num'])
    b.__dict__.update(test_answers)  # XXX: Consider using monkeypatch if psbl
    r = b.get_num(message)
    assert r.text == c.question.format(**test_answers)


def test_integration(monkeypatch, test_data):
    monkeypatch.setattr(time, 'ctime', lambda: 'testtime')
    expected = '{}{}{}'.format(
        c.query_date.format(current_time=b.time.ctime()),
        c.user_answers.format(**test_answers),
        c.user_data.format(**tud),
    )

    call = Call('yes')
    r = b.callback_worker(call)
    assert r.text == expected.strip()
