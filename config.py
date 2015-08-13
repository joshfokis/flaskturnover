import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/users'
SQLALCHEMY_BINDS = {
    'roles': 'mysql://username:password@localhost/roles',
    'client1': 'mysql://username:password@localhost/client1',
    'client2': 'mysql://username:password@localhost/client2',
    'client3': 'mysql://username:password@localhost/client3'
}


WTF_CSRF_ENABLED = True
SECRET_KEY = 'bacon'
