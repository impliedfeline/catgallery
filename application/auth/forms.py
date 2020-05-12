from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class SignupForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2, max=144)])
    password = PasswordField("Password", [
        validators.Length(min=2, max=144),
        validators.EqualTo("confirm", message="Passwords must match")
        ])
    confirm = PasswordField("Repeat password")

    class Meta:
        csrf = False
