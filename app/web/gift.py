from . import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from app.models.base import db
from flask import current_app, flash, redirect, url_for, render_template


@web.route("/my/gifts")
@login_required
def my_gifts():
    """@login_required用于授权登录
    但是需要@login_manager.user_loader装饰函数返回的user对象"""
    uid = current_user.id
    gifts = Gift.get_user_gifts(uid)
    isbn_lst = [gift.isbn for gift in gifts]
    wish_count_lst = Gift.get_wish_counts(isbn_lst)
    my_gifts = MyGifts(gifts, wish_count_lst)

    return render_template("my_gifts.html", gifts=my_gifts.gifts)


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
def redraw_from_gifts(gid):
    pass
