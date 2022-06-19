import re

from sqlalchemy import or_

from config import db, bot
from database import Task
from telegram_bot import messages as msg
from telegram_bot import keyboards as keys
from telegram_bot.decorators import user_exist


@bot.message_handler(commands=['start'])
@user_exist
def start(message, user):
    return bot.send_message(message.chat.id, msg.menu.format(user.tgid), reply_markup=keys.tasks())


@bot.callback_query_handler(func=lambda call: True)
@user_exist
def update(callback, user):
    bot.delete_message(callback.message.chat.id, callback.message.id)
    if re.fullmatch('close_[0-9]+', callback.data):
        task = db.session.query(Task).filter_by(id=callback.data.split('_')[1], userid=user.id).first()
        if task:
            task.status = False
            db.session.commit()
            return bot.send_message(callback.message.chat.id,
                                    msg.menu.format(str(callback.message.chat.id)+msg.task_close),
                                    reply_markup=keys.tasks())
        else:
            return bot.send_message(callback.message.chat.id,
                                    msg.menu.format(str(callback.message.chat.id)+msg.task_not_found),
                                    reply_markup=keys.tasks())

    if re.fullmatch('task_[0-9]+', callback.data):
        task = db.session.query(Task).filter_by(id=callback.data.split('_')[1], userid=user.id).first()
        if task:
            return bot.send_message(callback.message.chat.id, msg.task.format(task.id, task.title, task.body),
                                    reply_markup=keys.task(task.id))

    if re.fullmatch('add_task', callback.data):
        db.session.add(Task(userid=user.id, title='wait', status=False))
        db.session.commit()
        return bot.send_message(callback.message.chat.id, msg.task_titule)

    if callback.data == 'tasks':
        return bot.send_message(callback.message.chat.id, msg.menu.format(callback.message.chat.id),
                                reply_markup=keys.tasks())


@bot.message_handler()
@user_exist
def text(message, user):
    task = db.session.query(Task).filter(Task.userid == user.id, or_(Task.title == 'wait', Task.body == 'wait')).first()
    if task:
        if task.title == 'wait':
            task.title = message.text
            task.body = 'wait'
            db.session.commit()
            return bot.send_message(message.chat.id, msg.task_body)
        if task.body == 'wait':
            task.body = message.text
            task.status = True
            db.session.commit()
            return bot.send_message(user.tgid, msg.menu.format(user.tgid), reply_markup=keys.tasks())

