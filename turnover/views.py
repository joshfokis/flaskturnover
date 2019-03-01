from flask import (
    render_template, 
    flash, 
    redirect, 
    session, 
    url_for, 
    request, 
    g, 
    stream_with_context, 
    Response
)

from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
import datetime
from sqlalchemy import event
from flask_socketio import emit
from turnover import app, db, lm, socketio, admin
from .forms import (
    LoginForm, 
    EventForm, 
    EventViewForm, 
    RegistrationForm, 
    ForgotPassword, 
    PasswordReset, 
    SearchForm, 
    AlertForm
)

from .models import User, ClientEvents, Role, Alerts, Clients
from .util import send_email, ts
from config import ADMINS
from turnover import admin
import csv


@app.before_request
def before_request():
    """
    This is the check before requests are made to see if a user is authenticated, 
    get the session and set the forms
    """
    g.user = current_user
    try:
        if g.user.is_authenticated:
            g.user.lastlogin = datetime.datetime.now()
            db.session.add(g.user)
            db.session.commit()
    except:
        print('failed')
    addeventform = EventForm()
    print(addeventform)
    print(addeventform.clientlist.choices)
    alertform = AlertForm()


@lm.user_loader
def load_user(id):
    """
    Gets the user ID with the Login Manager
    """
    return User.query.get(int(id))


@app.errorhandler(404)
def not_found_error(error):
    """
    Allows a 404 error page to be displayed if a page is not found.
    """
    addeventform = EventForm()
    alertform = AlertForm()
    return render_template('404.html', addeventform=addeventform, alertform=alertform), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Allows a 500 error page to be displayed.
    """
    addeventform = EventForm()
    alertform = AlertForm()
    db.session.rollback()
    return render_template('500.html', addeventform=addeventform, alertform=alertform), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Creates the route for the login page.
    """
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is not None and user.verify_password(str(form.password.data)):
            login_user(user, form.remember_me.data)
            app.logger.debug('Logged in user %s' % user.username)
            return redirect(url_for('home'))
        else:
            error = " Wrong Username or Password"
            print(error)

    return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    """
    Creates the logout route.
    """
    logout_user()
    return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Creates the home\index route.
    This also sets the time for the add event along with the process of posting alerts and events
    """
    adderror = None
    viewform = EventViewForm()
    clients = Clients.query.all()
    #choices = [('test','test')]
    choices2 = [(row.id, row.client_name) for row in clients]
    print(choices2)
    try:
        viewform.client.choices += choices2
    except Exception as e:
        print(e)
    # print(viewform.client.choices)

    today = datetime.datetime.today()
    today2 = datetime.date.today()
    start_date = today2 + datetime.timedelta(days=3)
    end_date = today2
    posted = today.hour - 5
    count = 0

    posted1 = today - datetime.timedelta(
        hours=5, 
        minutes=today.minute, 
        seconds=today.second, 
        microseconds=today.microsecond
    )

    posted2 = '%i-%i-%i 23:59:59' % (today.year, today.month, today.day)
    posted3 = '%i-%i-%i 00:00:00' % (today.year, today.month, today.day)
    
    alerts = Alerts.query.filter(
        db.and_(
            (Alerts.startdate <= start_date),
            (Alerts.enddate >= end_date)
        )
    )

    user = str(g.user.username)
    addeventform = EventForm()
    try:
        addeventform.clientlist.choices += choices2
    except Exception as e:
        print(e)
    alertform = AlertForm()
    try:
        alertform.alert_client.choices += choices2
    except Exception as e:
        print(e)
    if alertform.validate_on_submit():

        alert = Alerts(
            title=alertform.alert_title.data, 
            client=alertform.alert_client.data, 
            details=alertform.alert_details.data, 
            startdate=alertform.alert_startdate.data,
            enddate=alertform.alert_enddate.data, 
            cleared=alertform.alert_cleared.data, 
            poster=user, 
            priority=alertform.alert_priority.data
        )

        db.session.add(alert)
        db.session.commit()

        return redirect(url_for('home'))

    if addeventform.validate_on_submit():

        #addeventform = EventForm()
        print(addeventform)
        post = ClientEvents(
            posted=datetime.datetime.now(),
            poster=user,
            event=addeventform.event.data,
            client=addeventform.clientlist.data
        )
        print(post)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))
    
    else:
        print('failed')
        post = ClientEvents(
            posted=datetime.datetime.now(),
            poster=user,
            event=addeventform.event.data,
            client=addeventform.clientlist.data
        )
        print('post: {}'.format(post))
    
    events = ClientEvents.query.filter(
        ClientEvents.posted.between(posted1,posted2)
    )

    return render_template(
        'home.html', 
        alertform=alertform, 
        addeventform=addeventform, 
        now=today.year, events=events, 
        viewform=viewform, 
        title='Summary', 
        alerts=alerts, 
        adderror=adderror,
        clients=clients
        )

@app.route('/turnoveremail', methods=['GET', 'POST'])
@login_required
def turnovercom():
    """
    creates the comercial turnover email page
    """
    today = datetime.datetime.today()
    user = str(g.user.username)
    addeventform = EventForm()
    alertform = AlertForm()
    today2 = datetime.date.today()
    start_date = today2 + datetime.timedelta(days=3)
    end_date = today2

    alertinfo = Alerts.query.filter(
        db.and_(
            (Alerts.startdate <= start_date),
            (Alerts.enddate >= end_date)
        )
    )

    events = ClientEvents.query.filter(
                ClientEvents.posted.between(
                    datetime.datetime.today() - datetime.timedelta(hours=12, minutes=30),
                    datetime.datetime.today()
                )
            )
    if alertform.validate_on_submit():

        alert = Alerts(
            title=alertform.alert_title.data, 
            client=alertform.alert_client.data, 
            details=alertform.alert_details.data, 
            startdate=alertform.alert_startdate.data,
            enddate=alertform.alert_enddate.data,
            cleared=alertform.alert_cleared.data, 
            poster=user, 
            priority=alertform.alert_priority.data, 
            ack=user
        )

        db.session.add(alert)
        db.session.commit()
        print(alert)

        return redirect(url_for('home'))

    if addeventform.validate_on_submit():

        addeventform = EventForm()
        post = ClientEvents(
            posted=datetime.datetime.now(), 
            poster=user, 
            event=addeventform.event.data, 
            client=addeventform.event.data
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        addeventform = EventForm()

    return render_template(
        'com.html', 
        events=events, 
        addeventform=addeventform, 
        alertform=alertform, 
        alertinfo=alertinfo
        )

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@app.route('/eventselect/', methods=['GET', 'POST'])
@login_required
def eventselect():
    """
    This creates the route to select what events to view.
    """
    today = datetime.datetime.today()
    posted1 = '%i-%i-%i 00:00:00' % (today.year, today.month, today.day)
    posted2 = '%i-%i-%i 23:59:59' % (today.year, today.month, today.day)
    clients = Clients.query.all()
    if request.method == "POST":
        eventview = request.values.get('eventview')
        

        print(eventview)

        if eventview == 'Summary':
            title = 'Summary'
            today = datetime.datetime.today()
            posted = today.hour - 5
    
            posted1 = '%i-%i-%i %i:00:00' % (today.year,
                                             today.month, today.day, posted)
    
            posted2 = '%i-%i-%i 23:59:59' % (today.year,
                                             today.month, today.day)
    
            events = ClientEvents.query.filter(
                ClientEvents.posted.between(posted1, posted2))
    
    
            return render_template('summary.html', events=events, clients=clients)
    
        else:
            print('event_select_else')
            title = Clients.query.filter_by(id=eventview).first()
            eventviewlogs = ClientEvents.query.filter(
                ClientEvents.posted.between(posted1, posted2),
                ClientEvents.client == eventview)
    
    else:
        eventviewlogs = []
        title = None
    
    return render_template('eventselect.html', eventviewlogs=eventviewlogs, title=title, client=eventview)

@app.route('/reset', methods=["GET", "POST"])
def reset():
    """
    This creates the password reset route
    """
    form = ForgotPassword()
    if form.validate_on_submit():
        emaildata = form.email.data.lower()
        user = User.query.filter_by(
            email=form.email.data).first_or_404()
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
    """
    Creates the route for the password reset link with a token
    """
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.password.data)
        print('password hash  ', generate_password_hash(form.password.data))
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data, role_id=0, active=True)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


DB_INSERT_EVENT = 'db.inserted'


@event.listens_for(ClientEvents, 'after_insert')
def events_after_insert(mapper, connection, target):
    """
    This is the event listener for the websocket to allow instant update without reloading.
    """
    # target should be an instance of EventsClient1, and depending on your
    # database and configuration, it's Primary Key should be populated as well
    print('listen event\n target: {},\n mapper: {},\n connection: {},'.format(target, mapper, connection))
    socketio.emit(DB_INSERT_EVENT, {
        'client': target.client,
        'event': target.event,
        'posted': target.posted.strftime('%Y-%m-%d %H:%M:%S'),
        'poster': str(target.poster)}, namespace='/test')

@socketio.on('connect', namespace='/test')
def test_connect():
    """
    Emits the data for the socket and listener
    """
    emit('my response', {'data': 'Connected'})


@app.route('/search/', methods=["GET", "POST"])
@login_required
def search(): 
    """
    The search route is created here.
    TODO:: Paginate the search view. 
    """
    warning = None
    form = SearchForm()
    clients = Clients.query.all()
    searchtext = form.search_box.data
    searchclient = form.client.data
    searchday = form.on_day.data
    searchstart = form.start_date.data
    searchend = form.end_date.data
    alertform = AlertForm()
    choices2 = [(row.id+1, row.client_name) for row in clients]
    form.client.choices += choices2

    if alertform.validate_on_submit():
        alert = Alerts(
            title=alertform.alert_title.data,
            client=alertform.alert_client.data,
            details=alertform.alert_details.data,
            startdate=alertform.alert_startdate.data,
            enddate=alertform.alert_enddate.data,
            cleared=alertform.alert_cleared.data,
            poster=user,
            priority=alertform.alert_priority.data
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return redirect(url_for('home'))
    user = str(g.user.username)
    addeventform = EventForm()
    
    if addeventform.validate_on_submit():
        addeventform = EventForm()

        post = CLientEvents(
            posted=datetime.datetime.now(), 
            poster=user, 
            event=addeventform.event.data,
            client=addeventform.event.data
        )

        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('home'))

    if form.validate_on_submit():
        print('form passed')
        if searchday != None:
            posted1 = '%i-%i-%i 00:00:00' % (
                searchday.year, searchday.month, searchday.day)
    
            posted2 = '%i-%i-%i 23:59:59' % (
                searchday.year, searchday.month, searchday.day)
    
            results = ClientEvents.query.filter(
                ClientEvents.posted.between(posted1, posted2),
                ClientEvents.client == searchclient-1)
    
        elif searchstart and searchend != None:
            searchend1 = searchend + datetime.timedelta(days=1)
            results = ClientEvents.query.filter(
                ClientEvents.posted.between(searchstart, searchend1),
                ClientEvents.client == searchclient-1)
    
        elif searchtext != '':
            results = ClientEvents.query.filter(
                ClientEvents.event.ilike('%' + searchtext + '%'),
                ClientEvents.client == searchclient-1)
    
        elif searchtext != '' and (searchstart and searchend) != None:
            searchend1 = searchend + datetime.timedelta(days=1)
            results = ClientEvents.query.filter(
                ClientEvents.posted.between(searchstart, searchend1),
                ClientEvents.client == searchclient-1
                ).filter(ClientEvents.event.ilike('%' + searchtext + '%'))
    
        elif searchtext != '' and searchday != None:
            posted1 = '%i-%i-%i 00:00:00' % (
                searchday.year, searchday.month, searchday.day)
            posted2 = '%i-%i-%i 23:59:59' % (
                searchday.year, searchday.month, searchday.day)
            results = ClientEvents.query.filter(ClientEvents.posted.between(
                posted1, posted2), ClientEvents.client == searchclient-1
                ).filter(ClientEvents.event.ilike('%' + searchtext + '%'))
    
        elif searchtext == '' and (searchstart and searchend) == None and searchday == None:
            results = None
            warning = "Please make sure the text, date, and/or start and end dates have data."

        return render_template(
            'search.html', 
            results=results, 
            form=form, 
            alertform=alertform, 
            addeventform=addeventform,
            warning=warning
        )
    else:
        print('form error: {}'.format(form.errors))
        print('searchday {}'.format(searchday))
        print('searchend {}'.format(searchend))
        print('searchstart {}'.format(searchstart))
        print('searchtext {}'.format(searchtext))
        print('searchclient {}'.format(searchclient))
        
    return render_template('search.html', form=form, alertform=alertform, addeventform=addeventform)

@app.route('/archive/', methods=["GET", "POST"])
@login_required
def archive():
    """
    Allows the selection of a date on the calendar to view events from that date.
    """
    datecal = request.values['datecal']
    today = datetime.datetime.today()
    posted1 = '%s-%s-%s 00:00:00' % (datecal[6:], datecal[0:2], datecal[3:5])
    posted2 = '%s-%s-%s 23:59:59' % (datecal[6:], datecal[0:2], datecal[3:5])
    events = ClientEvents.query.filter(
        ClientEvents.posted.between(posted1, posted2))
    return render_template('archive.html', now=today.year, events=events, title='Archive')
