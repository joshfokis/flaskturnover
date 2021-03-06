import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_wtf.csrf import CsrfProtect
from flask_socketio import SocketIO
from flask_admin import Admin

"""
This is the configurations for the applications and for Flask.
"""
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
moment = Moment(app)
CsrfProtect(app)
socketio = SocketIO(app)
mail = Mail(app)
admin = Admin(app, name='Turnover', template_mode='bootstrap3')


#if app.debug:
#    import logging
#    from logging.handlers import RotatingFileHandler
#    file_handler = RotatingFileHandler('tmp/Turnover.log', 'a', 1 * 1024 * 1024, 10)
#    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#    app.logger.setLevel(logging.INFO)
#    file_handler.setLevel(logging.INFO)
#    app.logger.addHandler(file_handler)
#    app.logger.info('Turnover startup')

from turnover import views, models
