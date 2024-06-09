from flask import jsonify, request
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
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


@web.route("/book/search2")
def search2():
    # 参数校验
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        # 通过form可以取得默认值
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == "isbn":
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page)

        return jsonify(result)

    return jsonify(form.errors)


@web.route("/book/info")
def info():
    """
    测试路由
    """
    return jsonify("hello")
