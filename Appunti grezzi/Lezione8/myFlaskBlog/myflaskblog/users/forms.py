#Users
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from myflaskblog.models import User

from flask_login import current_user


class RegistrationForm(FlaskForm):
    # Campo per l'username con lunghezza minima e massima, non può essere vuoto
    username = StringField('Username', validators=[
        Length(min=2, max=30), DataRequired()])
    # Campo per l'email con lunghezza minima e massima, deve essere una email valida, non può essere vuoto
    email = StringField('Email', validators=[
        Length(min=2, max=100), Email(), DataRequired()])
    # Campo per la password con lunghezza minima e massima, non può essere vuoto
    password = PasswordField('Password', validators=[
        Length(min=8, max=100), DataRequired()])
    # Campo per la conferma della password con lunghezza minima e massima, deve essere uguale alla password, non può essere vuoto
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=8, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    # Bottone per registrarsi
    submit = SubmitField('Register Now!')

    # Validazione email unica
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

    # Validazione username unico
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    # Campo per l'email con lunghezza minima e massima, deve essere una email valida, non può essere vuoto
    email = StringField('Email', validators=[
        Length(min=2, max=100), Email(), DataRequired()])
    # Campo per la password con lunghezza minima e massima, non può essere vuoto
    password = PasswordField('Password', validators=[
        Length(min=8, max=100), DataRequired()])
    # Checkbox per ricordarsi l'accesso
    remember_me = BooleanField('Remember Me')
    # Bottone per il login
    submit = SubmitField('Log In')


class UpdateUserForm(FlaskForm):
    # Campo per l'username con lunghezza minima e massima, non può essere vuoto
    username = StringField('Username', validators=[
        Length(min=2, max=30), DataRequired()])
    # Campo per l'email con lunghezza minima e massima, deve essere una email valida, non può essere vuoto
    email = StringField('Email', validators=[
        Length(min=2, max=100), Email(), DataRequired()])
    # Campo per caricare l'immagine dell'utente con estensioni ammesse
    image_file = FileField('Update your Avatar', validators=[
        FileAllowed(['jpg', 'png'])])
    # Bottone per aggiornare il profilo utente
    submit = SubmitField('Update Your Profile!')

    # Validazione email unica
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered')

    # Validazione username unico
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already registered')
