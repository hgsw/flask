from app import mail
from flask_mail import Message
from flask import current_app, render_template


def send_mail(to, subject, template, **kwargs):
    msg = Message("[鱼书]" + " " + subject, sender=current_app.config["MAIL_USERNAME"], recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(message=msg)


# def send_mail():
#     msg = Message("测试邮件", sender="hgsw93@163.com", body="Hello", recipients=["hgsw93@163.com"])
#     mail.send(message=msg)
#     pass
