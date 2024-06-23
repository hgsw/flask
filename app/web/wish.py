from . import web
from flask_login import login_required, current_user
from app.models.base import db
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from flask import flash, redirect, url_for, render_template


@web.route("/my/wish")
def my_wish():
    uid = current_user.id
    # 根据当前用户id查询所有书籍
    wishes = Wish.get_user_wishes(uid)
    isbn_lst = [wish.isbn for wish in wishes]
    wish_count_lst = Wish.get_gift_counts(isbn_lst)
    view_model = MyTrades(wishes, wish_count_lst)

    return render_template("my_wish.html", wishes=view_model.trade)


@web.route("/wish/book/<isbn>")
@login_required
def save_to_wish(isbn):
    # can_save_to_list 业务校验 检验isbn合法、书籍存在
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id

            db.session.add(wish)
    else:
        flash("图书已存在你的赠送清单或存在你的心愿清单，请勿重复添加")

    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route("/satisfy/wish/<int:wid>")
def satisfy_wish(wid):
    pass


@web.route("/wish/book/<isbn>/redraw")
def redraw_from_wish(isbn):
    pass
