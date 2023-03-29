# Main
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, EmailField
from wtforms import PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from myflaskblog.models import User

from flask_login import current_user

'''
Registrazione:
username
email
password
confirm_password

Login:
email
password
remembre_me
'''

