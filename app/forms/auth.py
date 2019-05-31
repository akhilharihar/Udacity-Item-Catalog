from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Email, Optional


class LoginForm(FlaskForm):
    email_id = StringField(
        'Email Address',
        validators=[DataRequired(), Email()]
    )
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', validators=[Optional()])
