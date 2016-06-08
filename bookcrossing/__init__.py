import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from bookcrossing.config import runtime_config


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# dev, prod, test
APP_STATUS = 'dev'

app = Flask(__name__)
app.config.from_object(runtime_config(APP_STATUS))

api = Api(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from bookcrossing import models, views, forms



