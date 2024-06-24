from . import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.view_models.trade import MyTrades
from app.models.base import db
from flask import current_app, flash, redirect, url_for, render_template
from app.models.drift import Drift
from app.libs.enums import PendingStatus


@web.route("/my/gifts")
@login_required
def my_gifts():
    """@login_required用于授权登录
    但是需要@login_manager.user_loader装饰函数返回的user对象"""
    uid = current_user.id
    # 根据当前用户id查询所有书籍
    gifts = Gift.get_user_gifts(uid)
    isbn_lst = [gift.isbn for gift in gifts]
    # 根据isbn查询想要此书籍的人
    wish_count_lst = Gift.get_wish_counts(isbn_lst)
    view_model = MyTrades(gifts, wish_count_lst)

    return render_template("my_gifts.html", gifts=view_model.trade)


@web.route("/gifts/book/<isbn>")
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            # 这里操作了两张表，需要事务处理，需要回滚
            gift = Gift()
            gift.isbn = isbn
            # current_user是实例化user的模型
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     # 如果不回滚会导致后面数据无法再操作
        #     db.session.rollback()
        #     raise e

        # 这里提交完成会跳转到当前页面是没有意义
        # ajax技术可以改善服务性能
        # book_detail模本渲染也是很消耗服务器性能
    else:
        flash("图书已存在你的赠送清单或存在你的心愿清单，请勿重复添加")

    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route("/gifts/<gid>/redraw")
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.waiting).first()
    if drift:
        flash("这个礼物正在处于交易状态，请前往鱼漂完成该交易")
    else:
        with db.auto_commit():
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            gift.delete()

    return redirect(url_for("web.my_gifts"))
