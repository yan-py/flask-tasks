from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, HiddenField, PasswordField


class TaskForm(FlaskForm):
    title = StringField("Title")
    body = TextAreaField("Body")
    submit = SubmitField("Add")


class CloseForm(FlaskForm):
    taskid = HiddenField()
    submit = SubmitField("Close")


class LoginForm(FlaskForm):
    login = StringField("Login")
    password = PasswordField("Password")
    submit = SubmitField("Login")
