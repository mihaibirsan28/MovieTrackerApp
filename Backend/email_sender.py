import os
from typing import List

from starlette.templating import Jinja2Templates

from display_messages import CONFIRMATION_EMAIL_CONTENT, CONFIRMATION_EMAIL_SUBJECT, CONFIRM_ACCOUNT_BUTTON_MESSAGE

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dotenv import load_dotenv

from models import User

load_dotenv('email.env')


class Environments:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME')


conf = ConnectionConfig(
    MAIL_USERNAME=Environments.MAIL_USERNAME,
    MAIL_PASSWORD=Environments.MAIL_PASSWORD,
    MAIL_FROM=Environments.MAIL_FROM,
    MAIL_PORT=Environments.MAIL_PORT,
    MAIL_SERVER=Environments.MAIL_SERVER,
    MAIL_FROM_NAME=Environments.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./templates'
)


def send_email(background_tasks: BackgroundTasks,
               subject: str, recipients: List[str], body: dict, email_template: str):
    message = MessageSchema(
        subject=subject, recipients=recipients, template_body=body, subtype=MessageType.html)
    fast_mail = FastMail(conf)
    background_tasks.add_task(fast_mail.send_message, message, template_name=email_template)


def send_account_confirmation_email(background_tasks: BackgroundTasks, user: User, confirmation_link: str):
    recipients = [user.email]
    send_email(background_tasks,
               CONFIRMATION_EMAIL_SUBJECT,
               recipients,
               {
                   'template_body':
                   {
                       'title': CONFIRMATION_EMAIL_SUBJECT,
                       'name': f'{user.first_name} {user.last_name}',
                       'message': CONFIRMATION_EMAIL_CONTENT,
                       'link': confirmation_link,
                       'button_message': CONFIRM_ACCOUNT_BUTTON_MESSAGE
                   }
               },
               'account_confirmation_email.html')
