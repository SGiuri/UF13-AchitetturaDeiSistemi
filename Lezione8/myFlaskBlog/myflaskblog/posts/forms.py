#Posts

from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired
from myflaskblog.models import User

from flask_login import current_user


class NewPostForm(FlaskForm):
    post_title = StringField('Post Title', validators=[
        Length(min=2, max=100), DataRequired()])
    post_content = TextAreaField('Post Content', validators=[DataRequired()])

    submit = SubmitField('Post Message')
