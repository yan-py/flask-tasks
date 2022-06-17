from telebot.types import CallbackQuery, Message
from config import db
from database import User
from telegram_bot.handler import bot
import telegram_bot.messages as msg


def user_exist(func):
    def wrapper(tg_msg):
        if isinstance(tg_msg, CallbackQuery):
            user = db.session.query(User).filter_by(tgid=tg_msg.message.chat.id).first()
            if not user:
                bot.send_message(tg_msg.message.chat.id, msg.new_user.format('http://127.0.0.1:5000'))
            else:
                func(tg_msg, user)
        if isinstance(tg_msg, Message):
            user = db.session.query(User).filter_by(tgid=tg_msg.chat.id).first()
            if not user:
                bot.send_message(tg_msg.chat.id, msg.new_user.format('http://127.0.0.1:5000'))
            else:
                func(tg_msg, user)
    return wrapper
