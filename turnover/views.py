from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime
from turnover import app, db, lm
from .forms import LoginForm, EventForm, EventViewForm, RegistrationForm
from .models import User, EventsClient1, EventsClient2, EventsClient3



@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(form.password.data)
        pwd = generate_password_hash(form.password.data)
        pwd2 = user.pwd_hash
        print(user)
        print(pwd, '\n', pwd2)
        print(user.verify_password(str(form.password.data)))
        if user is not None and user.verify_password(str(form.password.data)):
            print(user.verify_password(str(form.password.data)))
            login_user(user, form.remember_me.data)
            app.logger.debug('Logged in user %s', user.username)
            flash('Logged in user %s', user.username)
            return redirect(url_for('home'))
        error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    today = datetime.today()
    posted1 = '%i-%i-%i 00:00:00' % (today.year, today.month, today.day)
    posted2 = '%i-%i-%i 23:59:59' % (today.year, today.month, today.day)
    viewform = EventViewForm()
    events = EventsClient1.query.filter(EventsClient1.posted.between(posted1, posted2))
    return render_template('home.html', events=events, viewform=viewform)

@app.route('/eventselect/', methods=['GET', 'POST'])
def eventselect():
    today = datetime.today()
    posted1 = '%i-%i-%i 00:00:00' % (today.year, today.month, today.day)
    posted2 = '%i-%i-%i 23:59:59' % (today.year, today.month, today.day)
    if request.method == "POST":
        eventview = request.values['eventview']
        title = eventview
        if eventview == 'EventsClient1':
            eventview = EventsClient1
        elif eventview == 'EventsClient2':
            eventview = EventsClient2
        else:
            eventview = EventsClient3
        eventviewlogs = eventview.query.filter(eventview.posted.between(posted1, posted2))
    else:
        eventviewlogs = []
    return render_template('eventselect.html', eventviewlogs=eventviewlogs, title=title)

@app.route('/addevent', methods=['GET', 'POST'])
def addevent():
    user = str(g.user.username)
    form = EventForm()
    if form.validate_on_submit():
        form = EventForm()
        dbin = form.client.data
        print(dbin)
        if dbin == 'EventsClient1':
            dbin = EventsClient1
        elif dbin == 'EventsClient2':
            dbin = EventsClient2
        else:
            dbin = EventsClient3
        print(dbin)
        post = dbin(posted=datetime.utcnow(), poster=user, event=form.event.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        form = EventForm()
    return render_template('addevent.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.password.data)
        print('password hash  ', generate_password_hash(form.password.data))
        user = User(username=form.username.data, email=form.email.data,
                    pwd_hash=generate_password_hash(form.password.data), role_id=1, is_active=True)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
