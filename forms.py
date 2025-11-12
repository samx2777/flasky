import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp, EqualTo


def no_html_tags(form, field):  # noqa: ANN001
    value = field.data or ''
    if '<' in value or '>' in value:
        raise ValidationError('HTML tags are not allowed.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64), no_html_tags])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=80), no_html_tags])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField(
        'Phone',
        validators=[
            Length(max=20),
            Regexp(r'^[0-9+()\-\s]*$', message='Invalid phone number format.'),
        ],
    )
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000), no_html_tags])
    submit = SubmitField('Send')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64), no_html_tags])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')],
    )
    submit = SubmitField('Sign Up')

    def validate_username(self, field):  # noqa: ANN001
        # Local import to avoid circular dependency at module import time
        from models import User
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')

    def validate_email(self, field):  # noqa: ANN001
        from models import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')


