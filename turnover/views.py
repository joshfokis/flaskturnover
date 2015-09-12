from flask import render_template, flash, redirect, session, url_for, request, g, stream_with_context, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
import datetime
from sqlalchemy import event
from flask.ext.socketio import emit
from turnover import app, db, lm, socketio, admin
from .forms import LoginForm, EventForm, EventViewForm, RegistrationForm, ForgotPassword, PasswordReset, SearchForm, AlertForm
from .models import User, EventsClient1, EventsClient2, EventsClient3, Role, Alerts
from .util import send_email, ts
from config import ADMINS
import admin
import csv


@app.before_request
def before_request():
    g.user = current_user
    addeventform = EventForm()
    alertform = AlertForm()


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(404)
def not_found_error(error):
    addeventform = EventForm()
    alertform = AlertForm()
    return render_template('404.html', addeventform=addeventform, alertform=alertform), 404


@app.errorhandler(500)
def internal_error(error):
    addeventform = EventForm()
    alertform = AlertForm()
    db.session.rollback()
    return render_template('500.html', addeventform=addeventform, alertform=alertform), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(str(form.password.data)):
            login_user(user, form.remember_me.data)
            app.logger.debug('Logged in user %s' % user.username)
            return redirect(url_for('home'))
        else:
            error = " Wrong Username or Password"
            print error

    return render_template('login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    adderror = None
    viewform = EventViewForm()
    today = datetime.datetime.today()
    today2 = datetime.date.today()
    start_date = today2 + datetime.timedelta(days=3)
    end_date = today2
    posted = today.hour - 5
    count = 0
    posted1 = '%i-%i-%i %i:00:00' % (today.year,
                                     today.month, today.day, posted)
    posted2 = '%i-%i-%i 23:59:59' % (today.year, today.month, today.day)
    posted3 = '%i-%i-%i 00:00:00' % (today.year, today.month, today.day)
    alerts = Alerts.query.filter(
        db.and_(
            (Alerts.startdate <= start_date),
            (Alerts.enddate >= end_date)))
    user = str(g.user.username)
    addeventform = EventForm()
    alertform = AlertForm()
    if alertform.validate_on_submit():
        alert = Alerts(title=alertform.alert_title.data, client=alertform.alert_client.data, details=alertform.alert_details.data, startdate=alertform.alert_startdate.data,
                       enddate=alertform.alert_enddate.data, cleared=alertform.alert_cleared.data)
        db.session.add(alert)
        db.session.commit()
    if addeventform.validate_on_submit():
        addeventform = EventForm()
        if g.user.role_id != 3:
            dbin = addeventform.clientlist.data
            if dbin == 'EventsClient1':
                dbin = EventsClient1
            elif dbin == 'EventsClient2':
                dbin = EventsClient2
            elif dbin == 'all':
                clients = (EventsClient1, EventsClient2, EventsClient3)
                for i in clients:
                    post = i(
                        posted=today, poster=user, event=addeventform.event.data)
                    db.session.add(post)
                    db.session.commit()
                return redirect(url_for('home'))
            elif dbin == '':
                pass
                adderror = "You must select a client"
                return redirect(url_for('home'))
            else:
                dbin = EventsClient3
        else:
            dbin = EventsClient3
        post = dbin(
            posted=datetime.datetime.now(), poster=user, event=addeventform.event.data)
        db.session.add(post)
        db.session.commit()
    else:
        addeventform = EventForm()
    if g.user.role_id != 3:
        events = EventsClient1.query.filter(
            EventsClient1.posted.between(posted1, posted2))
        events2 = EventsClient2.query.filter(
            EventsClient2.posted.between(posted1, posted2))
        events3 = EventsClient3.query.filter(
            EventsClient3.posted.between(posted1, posted2))
        return render_template('home.html', alertform=alertform, addeventform=addeventform, now=today.year, events=events, events2=events2, events3=events3, viewform=viewform, title='Summary', alerts=alerts, adderror=adderror)
    else:
        for a in alerts:
            if a.cleared == False:
                count += 1
        events3 = EventsClient3.query.filter(
            EventsClient3.posted.between(posted3, posted2))
        return render_template('home.html', addeventform=addeventform, alertform=alertform, events3=events3, viewform=viewform, alerts=alerts, count=count, adderror=adderror)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@app.route('/eventselect/', methods=['GET', 'POST'])
@login_required
def eventselect():
    today = datetime.datetime.today()
    posted1 = '%i-%i-%i 00:00:00' % (today.year, today.month, today.day)
    posted2 = '%i-%i-%i 23:59:59' % (today.year, today.month, today.day)
    if request.method == "POST":
        eventview = request.values['eventview']
        title = eventview
        if eventview == 'EventsClient1':
            eventview = EventsClient1
        elif eventview == 'EventsClient2':
            eventview = EventsClient2
        elif eventview == 'Summary':
            today = datetime.datetime.today()
            posted = today.hour - 5
            posted1 = '%i-%i-%i %i:00:00' % (today.year,
                                             today.month, today.day, posted)
            posted2 = '%i-%i-%i 23:59:59' % (today.year,
                                             today.month, today.day)
            events = EventsClient1.query.filter(
                EventsClient1.posted.between(posted1, posted2))
            events2 = EventsClient2.query.filter(
                EventsClient2.posted.between(posted1, posted2))
            events3 = EventsClient3.query.filter(
                EventsClient3.posted.between(posted1, posted2))
            return render_template('summary.html', events=events, events2=events2, events3=events3, title=title)
        else:
            eventview = EventsClient3
        eventviewlogs = eventview.query.filter(
            eventview.posted.between(posted1, posted2))
    else:
        eventviewlogs = []
    return render_template('eventselect.html', eventviewlogs=eventviewlogs, title=title)


# @app.route('/addevent', methods=['GET', 'POST'])
# @login_required
# def addevent():
#     user = str(g.user.username)
#     form = EventForm()
#     if form.validate_on_submit():
#         form = EventForm()
#         if g.user.role_id != 3:
#             dbin = form.client.data
#             if dbin == 'EventsClient1':
#                 dbin = EventsClient1
#             elif dbin == 'EventsClient2':
#                 dbin = EventsClient2
#             else:
#                 dbin = EventsClient3
#         else:
#             dbin = EventsClient3
#         post = dbin(
#             posted=datetime.datetime.now(), poster=user, event=form.event.data)
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('home'))
#     else:
#         form = EventForm()
#     return render_template('addevent.html', form=form)


@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = ForgotPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        subject = "Password rest requested"
        token = ts.dumps(form.email.data, salt='recover-key')
        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)
        html = render_template(
            'email/recover.html',
            recover_url=recover_url)
        text = "password reset url"
        to = unicode(user.email)
        send_email(subject, None, [to], text, html)
        return redirect(url_for('home'))
    return render_template('reset.html', form=form)


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)
    form = PasswordReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_with_token.html', form=form, token=token)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         print(form.password.data)
#         print('password hash  ', generate_password_hash(form.password.data))
#         user = User(username=form.username.data, email=form.email.data,
#                     pwd_hash=generate_password_hash(form.password.data), role_id=1, is_active=True)
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template('register.html', form=form)

DB_INSERT_EVENT = 'db.inserted'


@event.listens_for(EventsClient1, 'after_insert')
def events_client1_after_insert(mapper, connection, target):
    # target should be an instance of EventsClient1, and depending on your
    # database and configuration, it's Primary Key should be populated as well
    socketio.emit(DB_INSERT_EVENT, {
        'client': 'client1',
        'event': target.event,
        'posted': target.posted.strftime('%Y-%m-%d %H:%M:%S'),
        'poster': str(target.poster)}, namespace='/test')


@event.listens_for(EventsClient2, 'after_insert')
def events_client2_after_insert(mapper, connection, target):
    # target should be an instance of EventsClient1, and depending on your
    # database and configuration, it's Primary Key should be populated as well
    socketio.emit(DB_INSERT_EVENT, {
        'client': 'client2',
        'event': target.event,
        'posted': target.posted.strftime('%Y-%m-%d %H:%M:%S'),
        'poster': str(target.poster)}, namespace='/test')


@event.listens_for(EventsClient3, 'after_insert')
def events_client3_after_insert(mapper, connection, target):
    # target should be an instance of EventsClient1, and depending on your
    # database and configuration, it's Primary Key should be populated as well
    socketio.emit(DB_INSERT_EVENT, {
        'client': 'client3',
        'event': target.event,
        'posted': target.posted.strftime('%Y-%m-%d %H:%M:%S'),
        'poster': str(target.poster)}, namespace='/test')


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@app.route('/search/', methods=["GET", "POST"])
@login_required
def search(page=1):
    form = SearchForm()
    searchtext = form.search_box.data
    searchclient = form.client.data
    searchday = form.on_day.data
    searchstart = form.start_date.data
    searchend = form.end_date.data
    alertform = AlertForm()
    if alertform.validate_on_submit():
        alert = Alerts(title=alertform.alert_title.data, client=alertform.alert_client.data, details=alertform.alert_details.data, startdate=alertform.alert_startdate.data,
                       enddate=alertform.alert_enddate.data, cleared=alertform.alert_cleared.data)
        db.session.add(alert)
        db.session.commit()
    user = str(g.user.username)
    addeventform = EventForm()
    if addeventform.validate_on_submit():
        addeventform = EventForm()
        if g.user.role_id != 3:
            dbin = addeventform.client.data
            if dbin == 'EventsClient1':
                dbin = EventsClient1
            elif dbin == 'EventsClient2':
                dbin = EventsClient2
            else:
                dbin = EventsClient3
        else:
            dbin = EventsClient3
        post = dbin(
            posted=datetime.datetime.now(), poster=user, event=addeventform.event.data)
        db.session.add(post)
        db.session.commit()

    if form.validate_on_submit():
        # searchtext = form.search_box.data
        # searchclient = form.client.data
        # searchday = form.on_day.data
        # searchstart = form.start_date.data
        # searchend = form.end_date.data
        # print('test', searchtext, searchday.year, searchday.month, searchday.day, searchstart, searchend)
        if g.user.role_id != 3:
            if searchclient == 'EventsClient1':
                searchclient = EventsClient1
            elif searchclient == 'EventsClient2':
                searchclient = EventsClient2
            elif searchclient == 'EventsClient3':
                searchclient = EventsClient3
            if searchday != None:
                posted1 = '%i-%i-%i 00:00:00' % (
                    searchday.year, searchday.month, searchday.day)
                posted2 = '%i-%i-%i 23:59:59' % (
                    searchday.year, searchday.month, searchday.day)
                results = searchclient.query.filter(
                    searchclient.posted.between(posted1, posted2))
            if searchstart and searchend != None:
                results = searchclient.query.filter(
                    searchclient.posted.between(searchstart, searchend))
            if searchtext != '':
                results = searchclient.query.filter(
                    searchclient.event.ilike('%' + searchtext + '%'))
            if searchtext != '' and (searchstart and searchend) != None:
                results = searchclient.query.filter(
                    searchclient.posted.between(searchstart, searchend)).filter(searchclient.event.ilike('%' + searchtext + '%'))
            if searchtext != '' and searchday != None:
                posted1 = '%i-%i-%i 00:00:00' % (
                    searchday.year, searchday.month, searchday.day)
                posted2 = '%i-%i-%i 23:59:59' % (
                    searchday.year, searchday.month, searchday.day)
                results = searchclient.query.filter(searchclient.posted.between(
                    posted1, posted2)).filter(searchclient.event.ilike('%' + searchtext + '%'))
            return render_template('search.html', results=results, form=form, alertform=alertform, addeventform=addeventform)
        else:
            searchclient = EventsClient3
            if searchday != None:
                posted1 = '%i-%i-%i 00:00:00' % (
                    searchday.year, searchday.month, searchday.day)
                posted2 = '%i-%i-%i 23:59:59' % (
                    searchday.year, searchday.month, searchday.day)
                results = searchclient.query.filter(
                    searchclient.posted.between(posted1, posted2))
                results = searchclient.query.filter(
                    searchclient.posted.between(searchstart, searchend))
            if searchtext != '':
                results = searchclient.query.filter(
                    searchclient.event.ilike('%' + searchtext + '%'))
            if searchtext != '' and (searchstart and searchend) != None:
                results = searchclient.query.filter(
                    searchclient.posted.between(searchstart, searchend)).filter(searchclient.event.ilike('%' + searchtext + '%'))
            if searchtext != '' and searchday != None:
                posted1 = '%i-%i-%i 00:00:00' % (
                    searchday.year, searchday.month, searchday.day)
                posted2 = '%i-%i-%i 23:59:59' % (
                    searchday.year, searchday.month, searchday.day)
                results = searchclient.query.filter(
                    searchclient.posted.between(posted1, posted2)).filter(searchclient.event.ilike('%' + searchtext + '%'))
            return render_template('search.html', results=results, form=form, alertform=alertform, addeventform=addeventform)
    return render_template('search.html', form=form, alertform=alertform, addeventform=addeventform)


# @app.route('/alerts', methods=["GET", "POST"])
# def alerts():
#     alertform = AlertForm()
#     if alertform.validate_on_submit():
#         alert = Alerts(title=alertform.alert_title.data, client=alertform.alert_client.data, details=alertform.alert_details.data, startdate=alertform.alert_startdate.data,
#                  enddate=alertform.alert_enddate.data, cleared=alertform.alert_cleared.data)
#         db.session.add(alert)
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template('addalert.html', alertform=alertform)

@app.route('/archive/', methods=["GET", "POST"])
@login_required
def archive():
    datecal = request.values['datecal']
    today = datetime.datetime.today()
    posted1 = '%s-%s-%s 00:00:00' % (datecal[6:], datecal[0:2], datecal[3:5])
    posted2 = '%s-%s-%s 23:59:59' % (datecal[6:], datecal[0:2], datecal[3:5])
    if g.user.role_id != 3:
        events = EventsClient1.query.filter(
            EventsClient1.posted.between(posted1, posted2))
        events2 = EventsClient2.query.filter(
            EventsClient2.posted.between(posted1, posted2))
        events3 = EventsClient3.query.filter(
            EventsClient3.posted.between(posted1, posted2))
        return render_template('archive.html', now=today.year, events=events, events2=events2, events3=events3, title='Archive')
    else:
        events3 = EventsClient3.query.filter(
            EventsClient3.posted.between(posted1, posted2))
        return render_template('archive.html', now=today.year, events3=events3, title='Archive')
