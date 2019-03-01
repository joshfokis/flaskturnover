import os
"""
Sets the base direcotry path for the Web Application.
"""
basedir = os.path.abspath(os.path.dirname(__file__))

"""
Set the SQL Database connections using the Flask SQLAlchemy URI. For more info visit http://flask-sqlalchemy.pocoo.org/2.1/config/
"""
SQLALCHEMY_DATABASE_URI = 'postgres://admin:password@databaseserver/flaskturnover'


"""
This will Set the allowed hosts to access the application, set debug, and WTForms CSRF.
"""

HOST = "0.0.0.0"
DEBUG = True
WTF_CSRF_ENABLED = True

"""
Secret Key for hashing. TODO better implementation/ hiding the Key.
"""
SECRET_KEY = 'secret'

"""
Configure the Mail server to send Password Recover Emails.
"""
MAIL_SERVER = 'smtp.email.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'user@email.com'
MAIL_PASSWORD = 'password'

# administrator list
ADMINS = ['user@email.com']
