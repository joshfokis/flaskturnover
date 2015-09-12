from werkzeug.security import generate_password_hash, check_password_hash
from turnover import db


class Alerts(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    client = db.Column(db.String(64))
    details = db.Column(db.String(500))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    cleared = db.Column(db.Boolean, default=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '%s' % (self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    pwd_hash = db.Column(db.String(200))
    email = db.Column(db.String(120), index=True, unique=True)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, password, email, active, role_id):
        self.username = username
        self.pwd_hash = generate_password_hash(password)
        self.email = email
        self.active = active
        self.role_id = role_id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def is_authenticated(self):
        # return self.authenticated
        return True

    def is_active(self):
        # return True
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '%s' % (self.username)

    def __unicode__(self):
        return '%s' % (self.username)

class EventsClient1(db.Model):
    __bind_key__ = 'client1'
    __tablename__ = 'client1'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(500))
    posted = db.Column(db.DateTime)
    poster = db.Column(db.String, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<EventsClient1 %r>' % (self.event)


class EventsClient2(db.Model):
    __bind_key__ = 'client2'
    __tablename__ ='client2'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(500))
    posted = db.Column(db.DateTime)
    poster = db.Column(db.String, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<EventsClient2 %r>' % (self.event)


class EventsClient3(db.Model):
    __bind_key__ = 'client3'
    __tablename__ ='client3'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(500))
    posted = db.Column(db.DateTime)
    poster = db.Column(db.String, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<EventsClient3 %r>' % (self.event)


