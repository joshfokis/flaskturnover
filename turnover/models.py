from werkzeug.security import generate_password_hash, check_password_hash
from turnover import db


class Alerts(db.Model):
    """
    This creates the Alerts table in the database.
    """
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    client = db.Column(db.String(64))
    details = db.Column(db.String(500))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    cleared = db.Column(db.Boolean, default=False)
    poster = db.Column(db.String(140))
    priority = db.Column(db.String(140))

class Clients(db.Model):
    __tablename__= 'client'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        """
        This returns the data as a string.
        """
        return '%s' % (self.client_name)

class Role(db.Model):
    """
    This creates the roles table in the database.
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    # users = []

    def __repr__(self):
        """
        This returns the data as a string.
        """
        return '%s' % (self.name)


class User(db.Model):
    """
    This creates the user table with the password and role ID.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    pwd_hash = db.Column(db.String(200))
    email = db.Column(db.String(120), index=True, unique=True)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # role_id = role_id
    lastlogin = db.Column(db.DateTime)

    def __init__(self, username, password, email, active, role_id):
        """
	    This returns the information from the table 
        """
        print('password: {}'.format(password))
        self.username = username.lower()
        self.pwd_hash = generate_password_hash(password)
        self.email = email
        self.active = active
        self.role_id = role_id
        # super(User,self).__init__()

    @property
    def password(self):
        """
        This sets the password as a property
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        This generates the password hash
        """
        self.pwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        This checks the password against the hash
        """
        print('hash: {}, password: {}'.format(self.pwd_hash, password))
        print('password_check: {}'.format(check_password_hash(self.pwd_hash, password)))
        return check_password_hash(self.pwd_hash, password)

    def is_authenticated(self):
        """
        Returns true if the user is authenticated
        """
        # return self.authenticated
        return True

    def is_active(self):
        """
        Returns true if active
        """
        # return True
        return self.active

    def is_anonymous(self):
        """
        Checks if user is anonymous
        """
        return False

    def get_id(self):
        """
        Try to use the unicode standard or return as string
        """
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '%s' % (self.username)

    def __unicode__(self):
        return '%s' % (self.username)

class ClientEvents(db.Model):
    """
    Creates the Educate events table in the database
    """
    # __bind_key__ = 'educate'
    __tablename__ = 'clientevents'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(500))
    posted = db.Column(db.DateTime)
    poster = db.Column(db.String(50))
    client = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
	    return '<ClientEvents %r>' % (self.event)
