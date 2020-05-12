# flask application
from flask import Flask
app = Flask(__name__)

# upload settings
from pathlib import Path
data = Path(__file__).resolve().parent.parent.joinpath("data")
data.mkdir(exist_ok=True)
app.config["UPLOAD_DIRECTORY"] = data
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}
app.config["THUMBNAIL_DIMENSIONS"] = 150, 150

# database settings
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pictures.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# models and views
from application import views

from application.pictures import models
from application.pictures import views

from application.auth import models
from application.auth import views

# login
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth login"
login_manager.login_message = "Please login to use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# creation of tables
db.create_all()
