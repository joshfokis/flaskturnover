from flask.ext.wtf import Form
from datetime import datetime
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, PasswordField, validators, DateField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Login')


class EventForm(Form):
    event = TextAreaField('Event Details', validators=[DataRequired()])
    clientlist = SelectField('client', choices=[('', 'Select Client'),('EventsClient1', 'Client 1'), ('EventsClient2', 'Client 2'), ('EventsClient3', 'Client 3'), ('all', 'All')])
    submit = SubmitField('ADD')


class EventViewForm(Form):
    client = SelectField('client', choices=[('Summary', 'Summary'),('EventsClient1', 'Client 1'), ('EventsClient2', 'Client 2'), ('EventsClient3', 'Client 3')])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class ForgotPassword(Form):
    email = StringField('Email Address', (validators.Required(), validators.Email()))
    submit = SubmitField('Submit')

class PasswordReset(Form):
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class AlertForm(Form):
    alert_title = StringField('Alert Title', [validators.Required(), validators.Length(min=4, max=140)])
    alert_client = StringField('Client', [validators.optional()])
    alert_details = TextAreaField('Details', validators=[DataRequired()])
    alert_startdate = DateField('Start Date', validators=[DataRequired()])
    alert_enddate = DateField('End Date', validators=[DataRequired()])
    alert_cleared = BooleanField('Cleared only', default=False)

class SearchForm(Form):
    search_box = StringField('Text', [validators.optional()])
    on_day = DateField('Date', [validators.optional()])
    start_date = DateField('Start Date', [validators.optional()])
    end_date = DateField('End Date', [validators.optional()])
    client = SelectField('client', choices=[('EventsClient1', 'Client 1'), ('EventsClient2', 'Client 2'), ('EventsClient3', 'Client 3')])
