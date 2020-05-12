from flask import flash, redirect, render_template, request, url_for, send_from_directory
from flask_login import login_required

from pathlib import Path
from PIL import Image

from application import app, db
from application.pictures.models import Picture
from application.pictures.forms import PictureForm

@app.route("/pictures/", methods=["GET"])
def pictures_index():
    return render_template("pictures/list.html", pictures = Picture.query.all())

@app.route("/pictures/new/")
@login_required
def pictures_form():
    return render_template("pictures/new.html", form = PictureForm())

@app.route("/pictures/<picture_id>/", methods=["GET"])
def picture_show(picture_id):
    return render_template("pictures/show.html", picture =
            Picture.query.get(picture_id))

@app.route("/data/<filename>")
def send_image(filename):
    mimetype = get_mimetype(filename)
    return send_from_directory(directory=app.config["UPLOAD_DIRECTORY"],
            filename=filename,
            mimetype=mimetype)

@app.route("/pictures/", methods=["POST"])
@login_required
def pictures_create():
    form = PictureForm()

    if not form.validate():
        return render_template("pictures/new.html", form = form)

    p = Picture()

    db.session().add(p)
    db.session().flush()
    handle_file(form.file.data, p.id)
    db.session().commit()

    return redirect(url_for("pictures_index"))

def handle_file(file, picture_id):
    filename = str(picture_id)
    file.save(app.config["UPLOAD_DIRECTORY"].joinpath(filename))
    generate_thumbnail(filename)

def generate_thumbnail(filename):
    with open_image(filename) as image:
        filetype = image.format
        image.thumbnail((150, 150))
        image.save(app.config["UPLOAD_DIRECTORY"].joinpath(filename + ".thumb"),
                filetype)

def get_mimetype(filename):
    with open_image(filename) as image:
        return Image.MIME[image.format]

def open_image(filename):
    return Image.open(app.config["UPLOAD_DIRECTORY"].joinpath(filename))

