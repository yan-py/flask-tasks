from config import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    tgid = db.Column(db.Integer)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    title = db.Column(db.String(256), nullable=False, default='No title')
    body = db.Column(db.Text, nullable=False, default='No body')
    status = db.Column(db.Boolean, nullable=False, default=True)


def tasks_select(userid, active=True):
    res = Task.query.filter_by(userid=userid, status=active).all()
    return res


def close_task(userid, taskid):
    task = Task.query.filter_by(id=taskid, userid=userid).first()
    task.status = False
    db.session.commit()


def delete_task(userid, taskid):
    Task.query.filter_by(id=taskid, userid=userid).delete()
    db.session.commit()


def add_task(userid, title, body):
    task = Task(userid=userid, title=title, body=body)
    db.session.add(task)
    db.session.commit()


def add_user(login, password, tgid=0):
    user = User(login=login, password=generate_password_hash(password), tgid=tgid)
    db.session.add(user)
    db.session.commit()
    return user


def get_user(userid):
    return User.query.filter_by(id=userid).first()


def get_user_by_login(login):
    return User.query.filter_by(login=login).first()


if __name__ == '__main__':
    db.create_all()
    add_user('user', 'user', 0)
