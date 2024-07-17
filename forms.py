"""Forms for playlist app."""

from wtforms import StringField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class UserForm(FlaskForm):
    """Form for registering users."""

    username = StringField('Name', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()], render_kw={"type": "password"})
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
