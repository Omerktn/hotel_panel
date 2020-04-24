from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets

APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'dcde5facb64a33a337bea5254bcbe81ffdf25577880bd94a7b64bbfb79464cc3'
APP.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(APP)
bcrypt = Bcrypt(APP)
login_manager = LoginManager(APP)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from hotelpanel import routes
