import telebot
from config import db, tg_token
from database import User, Task
from telegram_bot import messages as msg
from telegram_bot import keyboards as keys

bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def start(message):
    user = db.session.query(User).filter_by(tgid=message.chat.id).first()
    if user:
        return bot.send_message(message.chat.id, msg.menu.format(user.tgid), reply_markup=keys.tasks())
    else:
        return bot.send_message(message.chat.id, msg.new_user.format('http://127.0.0.1:5000'))


@bot.callback_query_handler(func=lambda call: True)
def update(callback):
    bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data.startswith('close_'):
        # TODO: check if user own this task
        task = db.session.query(Task).filter_by(id=callback.data.split('_')[1]).first()
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

    if callback.data.startswith('task_'):
        # TODO: check if user own this task
        task = db.session.query(Task).filter_by(id=callback.data.split('_')[1]).first()
        if task:
            return bot.send_message(callback.message.chat.id, msg.task.format(task.id, task.title, task.body),
                                    reply_markup=keys.task(task.id))

    if callback.data == 'tasks':
        return bot.send_message(callback.message.chat.id, msg.menu.format(callback.message.chat.id),
                                reply_markup=keys.tasks())
