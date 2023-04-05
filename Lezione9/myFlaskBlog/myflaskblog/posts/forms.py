#Posts

from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class NewPostForm(FlaskForm):
    post_title = StringField('Post Title', validators=[
        Length(min=2, max=100), DataRequired()])
    post_content = TextAreaField('Post Content', validators=[DataRequired()])

    submit = SubmitField('Post Message')
