from flask_mail import Message
from threading import Thread
from app import mail, app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
               args=(app, msg)).start()
