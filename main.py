from flask import render_template, redirect, url_for
from werkzeug.security import check_password_hash

from config import app, login_manager
from forms import TaskForm, CloseForm, LoginForm, SignupForm
from flask_login import login_required, login_user, current_user
import database as db
from login import UserLogin
from threading import Thread
from telegram_bot.handler import bot


@app.errorhandler(500)
def server_error(a):
    return redirect(url_for('login'))


@app.errorhandler(404)
def file_not_found(a):
    return redirect(url_for('login'))


@app.errorhandler(401)
def unauthorized(a):
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().get(user_id)


@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_login(form.login.data)
        if user and check_password_hash(user.password, form.password.data):
            user_login = UserLogin().create(user)
            login_user(user_login, remember=False)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = db.add_user(form.username.data, form.password.data, form.tgid.data)
        user_login = UserLogin().create(user)
        login_user(user_login, remember=True)
        return redirect(url_for('dashboard'))
    return render_template('signup.html', form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    tasks = db.tasks_select(current_user._UserLogin__user.id)
    tasks.reverse()
    form = CloseForm()
    return render_template('dashboard.html', tasks=tasks, form=form, page='dashboard')


@app.route("/add", methods=['POST', 'GET'])
@login_required
def add():
    form = TaskForm()
    if form.validate_on_submit():
        db.add_task(current_user._UserLogin__user.id, form.title.data, form.body.data)
        return redirect(url_for('dashboard'))
    return render_template('add.html', form=form, page='add')


@app.route("/close", methods=['POST'])
@login_required
def close():
    form = CloseForm()
    if form.validate_on_submit():
        db.close_task(current_user._UserLogin__user.id, form.taskid.data)
    return redirect(url_for('dashboard'))


@app.route("/trash", methods=['POST', 'GET'])
@login_required
def trash():
    tasks = db.tasks_select(current_user._UserLogin__user.id, active=False)
    tasks.reverse()
    return render_template('trash.html', tasks=tasks, page='trash')


if __name__ == "__main__":
    Thread(target=bot.polling).start()
    app.run()
