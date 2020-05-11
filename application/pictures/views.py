from application import app, db
from flask import flash, redirect, render_template, request, url_for, send_from_directory
from application.pictures.models import Picture
from pathlib import Path

import imghdr

@app.route("/pictures/", methods=["GET"])
def pictures_index():
    return render_template("pictures/list.html", pictures = Picture.query.all())

@app.route("/pictures/new/")
def pictures_form():
    return render_template("pictures/new.html")

@app.route("/pictures/<picture_id>/", methods=["GET"])
def picture_show(picture_id):
    return render_template("pictures/show.html", picture =
            Picture.query.get(picture_id))

@app.route("/data/<picture_id>")
def send_image(picture_id):
    filename = str(picture_id)
    mimetype = get_mimetype(filename)
    return send_from_directory(directory=app.config["UPLOAD_DIRECTORY"],
            filename=filename,
            mimetype=mimetype)

@app.route("/pictures/", methods=["POST"])
def pictures_create():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file):
        p = Picture()

        db.session().add(p)
        db.session().flush()
        file.save(app.config["UPLOAD_DIRECTORY"].joinpath(str(p.id)))
        db.session().commit()

        return redirect(url_for("pictures_index"))

def allowed_file(file):
    return imghdr.what(file) in app.config["ALLOWED_EXTENSIONS"]

# Assumes file behind 'filename' is in a recognizable image format, which should
# be guaranteed by the use of 'allowed_file' in the upload process
def get_mimetype(filename):
    with open(app.config["UPLOAD_DIRECTORY"].joinpath(filename), "rb") as file:
        return "image/" + imghdr.what(file)

