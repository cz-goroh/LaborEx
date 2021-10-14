from LaborEx.celery import app
from django.core.mail import get_connection, send_mail
from django.conf import settings
from time import sleep
import logging

logging.basicConfig(filename="task_book.log", level=logging.INFO)

@app.task
def test1():
    sleep(10)
    print('test')

@app.task
def snd_mail_task(subject, text_content, to_tuple, html_message):
    # pddoeorozbvanykh
    connection = get_connection(
        host='smtp.yandex.ru',
        port=587,
        username='support@proofex.ru',
        password=settings.YANDEX_PASS,
        use_tls=True
    )
    s = send_mail(
        subject,# subject,
        text_content,
        'support@proofex.ru',
        to_tuple,
        connection=connection,
        html_message=html_message
    )
