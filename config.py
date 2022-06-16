from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
tg_token = ''
db = SQLAlchemy(app)
login_manager = LoginManager(app)
