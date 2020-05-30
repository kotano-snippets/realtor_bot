import pytest

import bot as b
import config
import content as c


# NOTE: Test time may vary depending on connection speed
# and server availability.

testbot_username = '@rieltor_spbstu_bot'
test_token = '1034733347:AAFFVYmKbVAVnz3GvTLXF5BOCOr8iCuTkzE'
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


@pytest.fixture
def provide_data(monkeypatch):
    '''Patch input data and return tuple(id, answers)'''
    monkeypatch.setattr(config, 'admin', test_id)
    monkeypatch.setattr(b, 'answers', test_answers)
    return test_id, test_answers


def test_start():
    message = Message('/start')
    r = b.start_message(message)
    assert r.text == c.welcome_message.strip()


def test_cancel():
    message = Message('отменить')
    r = b.get_name(message)
    assert r.text == message.text


def test_get_num():
    message = Message(test_answers['num'])
    b.answers.update(test_answers)  # XXX: Consider using monkeypatch if psbl
    r = b.get_num(message)
    assert r.text == c.question.format(**test_answers)


def test_integration(monkeypatch, provide_data):
    monkeypatch.setattr(b, 'ctime', lambda: 'testtime')
    expected = '{}{}{}'.format(
        c.query_date.format(current_time=b.ctime()),
        c.user_answers.format(**test_answers),
        c.user_data.format(**tud),
    )

    call = Call('yes')
    r = b.callback_worker(call)
    assert r.text == expected.strip()


pytest.main()
