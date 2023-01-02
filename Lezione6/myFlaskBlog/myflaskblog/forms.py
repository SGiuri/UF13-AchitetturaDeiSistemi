# Preparazione Lezione 5

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from myflaskblog.models import User
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


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[
                           Length(min=2, max=30), DataRequired()])
#    email = EmailField('email', validators=[Length(2, 100)])
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=8, max=100), DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=8, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register Now!')

    # def validate_field(self, field):
    #     if True:
    #         raise ValdationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=8, max=100), DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
