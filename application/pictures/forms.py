from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import ValidationError

from PIL import Image

def validate_filetype(form, field):
    with Image.open(field.data) as image:
        filetype = image.format
    field.data.seek(0)
    if not filetype in {"PNG", "JPEG"}:
        raise ValidationError("Illegal filetype (must be png or jpg)")

def validate_filesize(form, field):
    filesize = len(field.data.read())
    field.data.seek(0)
    max_filesize = 15728640
    if filesize > max_filesize:
        raise ValidationError("File too large")

def validate_image_dimensions(form, field):
    with Image.open(field.data) as image:
        width, height = image.size
    field.data.seek(0)
    if width < 500 or height < 500:
        raise ValidationError("Image dimensions too small (must be atleast 500x500)")

class PictureForm(FlaskForm):
    file = FileField(validators=[
        FileRequired(),
        validate_filetype,
        validate_filesize,
        validate_image_dimensions])

    class Meta:
        csrf = False
  
