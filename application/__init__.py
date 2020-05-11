from flask import Flask
app = Flask(__name__)

from pathlib import Path
uploads = Path(__file__).resolve().parent.parent.joinpath("uploads")
uploads.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = uploads
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pictures.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from application import views

from application.pictures import models
from application.pictures import views

db.create_all()
