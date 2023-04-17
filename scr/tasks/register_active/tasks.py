import smtplib
from email.message import EmailMessage

from models import User
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


celery = Celery('send_email', broker='redis://localhost:6379')


def get_email_template_register(password, email, username):
    print(email)
    msg = EmailMessage()
    msg['Subject'] = 'Find relatives'
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER

    msg.set_content(
        '<div>'
            f'<h1> Hello, {username}! You have registered on the site "Find Relatives" to activate your account, click on the <a href=http://127.0.0.1:8000/auth/activate/?h_password={password}&email={email}>link</a>. </h1>'
            "<h1> If you haven't done so, DO NOT click on the link. </h1>"
        '/<div>',
        subtype='html'
    )
    return msg

@celery.task
def send_email_register(password, email, username):
    email = get_email_template_register(password, email, username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


# f"http://127.0.0.1:8000/auth/activate/?h_password={password}&email={email}"
