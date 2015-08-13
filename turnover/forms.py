from flask.ext.wtf import Form
from datetime import datetime
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Login')


class EventForm(Form):
    event = TextAreaField('event', validators=[DataRequired()])
    client = SelectField('client', choices=[('EventsClient1', 'Client 1'), ('EventsClient2', 'Client 2'), ('EventsClient3', 'Client 3')])
    submit = SubmitField('ADD')


class EventViewForm(Form):
    client = SelectField('client', choices=[('EventsClient1', 'Client 1'), ('EventsClient2', 'Client 2'), ('EventsClient3', 'Client 3')])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
