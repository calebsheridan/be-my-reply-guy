from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, URL

class TweetForm(FlaskForm):
    tweet_url = StringField('Tweet URL', validators=[
        DataRequired(),
        URL(message="Please enter a valid URL")
    ])
