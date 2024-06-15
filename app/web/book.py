from flask import jsonify, request, render_template, flash
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookCollection
import json

from . import web

# # 调用方式 curl -i localhost:5001/http://127.0.0.1:5000/book/search/9787501524044/1
# # Get 请求参数在url中的路由定义
# @web.route("/book/search/<q>/<page>")
# def search(q, page):
#     # q: 关键字或isbn
#     # page: 查询页数
#     isbn_or_key = is_isbn_or_key(q)
#     if isbn_or_key == "isbn":
#         result = YuShuBook.search_by_isbn(q)
#     else:
#         result = YuShuBook.search_by_keyword(q)

#     return jsonify(result)
#     # return json.dumps(result), 200, {"content-type": "application/json"}


"""
这里有一个问题，request只是一个变量
当同时有不同的请求过来时，request如何区分不同请求所带的参数呢
单线程：比较简单，请求进来会是实例化一个request，其他请求需要排队（再实例化一个request）
多线程：短时间内多个请求进来，我们是无法区别request请求的，当修改request指向的数据，可能会造成数据的污染
多线程使用线程隔离，将不同的请求保存在字典中，key是线程的id号，value是request实例对象 参考 test/test3.py
"""


@web.route("/book/search")
def search():
    # 参数校验
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        # 通过form可以取得默认值
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == "isbn":
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)
        books.fill(yushu_book, q)

        # return json.dumps(books, default=lambda o: o.__dict__, ensure_ascii=False)
    else:
        flash("关键字不存在，重新输入")
        
    return render_template("search_result.html", books=books)


@web.route("/book/<isbn>/detail")
def book_detail():
    pass

@web.route("/book/info")
def info():
    """
    测试路由
    """
    return jsonify("hello")

