import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask.ext.login import LoginManager

from flask_restful import Api

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'users.db'

app = Flask(__name__)
# bookcrossing.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# bookcrossing.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['STATIC_FOLDER'] = os.path.join(BASE_DIR, 'static')
app.config['SECRET_KEY'] = 'some secret key here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from bookcrossing import models, views, forms



