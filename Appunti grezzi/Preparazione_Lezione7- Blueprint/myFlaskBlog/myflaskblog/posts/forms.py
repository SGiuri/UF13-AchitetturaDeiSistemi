from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired


class New_Post_Form(FlaskForm):
    title = StringField('Post Title', validators=[
                        Length(min=2, max=100), DataRequired()])
    post_content = TextAreaField('Write new Post', validators=[DataRequired()])

    submit = SubmitField('Post Message')


class Edit_Post_Form(FlaskForm):
    title = StringField('Post Title', validators=[
                        Length(min=2, max=100), DataRequired()])
    post_content = TextAreaField('Write new Post', validators=[DataRequired()])

    submit = SubmitField('Update Message')
    delete = SubmitField('Delete Message')
    rusure = SubmitField('Are you Sure ?')
