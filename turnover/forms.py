from flask_wtf import Form
from datetime import datetime
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, PasswordField, validators, DateField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    """
    This class creates the login form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Login')


class EventForm(Form):
    """
    This class creates the event form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    event = TextAreaField('Event Details', validators=[DataRequired()])
    clientlist = SelectField('client', coerce=int, choices=[])
    submit = SubmitField('ADD')


class EventViewForm(Form):    
    """
    This class creates the event view form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    client = SelectField('client', choices=[('Summary','Summary')])


class RegistrationForm(Form):
    """
    This class creates the Registration form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class ForgotPassword(Form):
    """
    This class creates the forgot password form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    email = StringField('Email Address', (validators.Required(), validators.Email()))
    submit = SubmitField('Submit')

class PasswordReset(Form):
    """
    This class creates the password reset form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class AlertForm(Form):
    """
    This class creates the alert form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    alert_title = StringField('Alert Title', [validators.Required(), validators.Length(min=4, max=140)])
    alert_client = SelectField('Client', [validators.optional()], coerce=int, choices=[])
    alert_details = TextAreaField('Details', validators=[DataRequired()])
    alert_startdate = DateField('Start Date', validators=[DataRequired()])
    alert_enddate = DateField('End Date', validators=[DataRequired()])
    alert_cleared = BooleanField('Cleared only', default=False)
    alert_priority = SelectField('Alert Type', choices=[('Informational', 'Informational'), ('High','High')])

class SearchForm(Form):
    """
    This class creates the Search form. For mor info visit https://flask-wtf.readthedocs.io/en/stable/
    """
    search_box = StringField('Text', [validators.optional()])
    on_day = DateField('Date', [validators.optional()])
    start_date = DateField('Start Date', [validators.optional()])
    end_date = DateField('End Date', [validators.optional()])
    client = SelectField('Client', coerce=int, choices=[], validators=[DataRequired()])
