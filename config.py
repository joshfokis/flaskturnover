import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://host:password@localhost/users'
SQLALCHEMY_BINDS = {
    'roles': 'mysql://host:password@localhost/roles',
    'alerts': 'mysql://host:password@localhost/alerts',
    'client1': 'mysql://host:password@localhost/client1',
    'client2': 'mysql://host:password@localhost/client2',
    'client3': 'mysql://host:password@localhost/client3'
}

HOST = "0.0.0.0"
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'

MAIL_SERVER = 'smtp.mailserver.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['admin@example.com']
