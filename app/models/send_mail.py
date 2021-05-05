from threading import Thread

from flask import current_app
from flask_mail import Message
from flask_security import MailUtil





# def send_async_email(app, msg):
#     with app.app_context():
#         # block only for testing parallel thread
#         # for i in range(10, -1, -1):
#         #     sleep(2)
#         #     print('time:', i)
#         print('====> sending async')
#         mail.send(msg)


# def send_email(subject, sender, recipients, text_body, html_body):
#     app = current_app._get_current_object()
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     # mail.send(msg)
#
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()


