from . import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from flask import flash, redirect, url_for, render_template, request
from app.forms.book import DriftForm
from app.models.base import db
from app.models.drift import Drift
from app.view_models.book import BookViewModel
from sqlalchemy.sql import or_
from sqlalchemy import desc
from app.view_models.drift import DriftCollection


@web.route("/drift/<int:gid>", methods=["GET", "POST"])
@login_required
def send_drift(gid):
    from app.libs.email import send_mail

    # 自己不能向自己索要礼物
    # 鱼豆必须足够，大于等于1
    # 每送出2本书，自己才可以向他人所有一本书
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash("这本书是你自己的，不能向自己索要书籍")
        return redirect(url_for("web.book_detail", isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    if not can:
        return render_template("not_enough_beans.html", beans=current_user.beans)

    form = DriftForm(request.form)

    if request.method == "POST" and form.validate():
        save_drift(form, current_gift)
        send_mail(
            current_gift.user.email, "有人想要一本书", "email/get_gift.html", wisher=current_user, gift=current_gift
        )
    gifter = current_gift.user.summary

    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans, form=form)


@web.route("/pending")
@login_required
def pending():
    drifts = (
        Drift.query.filter(or_(Drift.requester_id == current_user.id, Drift.gift_id == current_user.id))
        .order_by(Drift.create_time.desc())
        .all()
    )
    views = DriftCollection(drifts, current_user.id)
    return render_template("pending.html", drifts=views.data)


@web.route("/drift/<int:did>/reject")
def reject_drift(did):
    pass


@web.route("/drift/<int:did>/redraw")
def redraw_drift(did):
    pass


@web.route("/drift/<int:did>/mailed")
def mailed_drift(did):
    pass


def save_drift(drift_form, current_gift):
    from app.libs.email import send_mail

    with db.auto_commit():
        book = BookViewModel(current_gift.book)
        drift = Drift()
        # 将drift_form同名属性赋值到drift中
        drift_form.populate_obj(drift)
        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        # 当请求生成时，不需要让这个礼物处于锁定状态
        # 这样赠送者是可以收到多个索取请求的，由赠送者选择送给谁
        # current_gift.launched = True
        # 请求者鱼豆-1
        current_user.beans -= 1
        # 但是赠送者鱼豆不会立刻+1
        # current_gift.user.beans += 1
        db.session.add(drift)
