from app import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    msg = Message("[鱼书]" + " " + subject, sender=current_app.config["MAIL_USERNAME"], recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取flask真实的对象，而不是代理对象，原始是因为线程隔离导致代理对象获取不到
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


# def send_mail():
#     msg = Message("测试邮件", sender="hgsw93@163.com", body="Hello", recipients=["hgsw93@163.com"])
#     mail.send(message=msg)
#     pass
