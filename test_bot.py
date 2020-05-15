import pytest
import bot as b
from config import token, admin
import content as c


class Dct(dict):
    pass


class Message(Dct):
    def __init__(self, text):
        self.text = text
        self.chat = Dct()
        self.from_user = Dct()
        self.chat.id = admin
        self.from_user.id = admin


# TODO: figure out how to reduce connection time
@pytest.fixture
def return_bot():
    bot = b.telebot.TeleBot(token)
    bot.polling()
    return bot


def test_start():
    message = Message('/start')
    r = b.start_message(message)
    assert r.text == c.welcome_message.strip()
