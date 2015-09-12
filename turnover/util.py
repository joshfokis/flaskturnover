from itsdangerous import URLSafeTimedSerializer
from flask.ext.mail import Message
from turnover import app, mail
from config import ADMINS

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def send_email(subject, sender, recipients, text_body, html_body):
    if sender == None:
        sender= ADMINS[0]
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
