# Lezione 5

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField
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
                           Length(min=2, max=50), DataRequired()])
#    email = EmailField('email', validators=[Length(2, 100)])
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=2, max=100), DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=2, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register Now!')

    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('ValidationMessage')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already registered')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=2, max=100), DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateForm(FlaskForm):

    username = StringField('Username', validators=[
                           Length(min=2, max=50), DataRequired()])
#    email = EmailField('email', validators=[Length(2, 100)])
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])

    image_file = FileField('Profile Picture', validators=[
                           FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update Now!')

    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('ValidationMessage')
    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already registered')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered')


class New_Post_Form(FlaskForm):
    title = StringField('Post Title', validators=[
                        Length(min=2, max=100), DataRequired()])
    post_content = TextAreaField('Write new Post', validators=[DataRequired()])

    submit = SubmitField('Post Message')


class PasswordRecoveryRequestForm(FlaskForm):

    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])

    submit = SubmitField('Reset your password')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError('Email not registered')


class ResetPasswordForm(FlaskForm):

    password = PasswordField('New Password', validators=[
                             Length(min=2, max=100), DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[Length(min=2, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Change your password')


