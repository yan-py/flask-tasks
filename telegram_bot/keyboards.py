from config import db
from telebot import types
from database import Task


def tasks():
    markup = types.InlineKeyboardMarkup()
    for index, task in enumerate(db.session.query(Task).filter_by(status=True).all()):
        markup.row(types.InlineKeyboardButton(task.title[:25], callback_data=f'task_{task.id}'))
    markup.row(types.InlineKeyboardButton('Update', callback_data='tasks'))
    return markup


def task(taskid):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Close', callback_data=f'close_{taskid}'))
    markup.row(types.InlineKeyboardButton('Back', callback_data='tasks'))
    return markup
