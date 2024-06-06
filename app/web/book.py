from flask import jsonify, Blueprint
from helper import is_isbn_or_key
from yushu_book import YuShuBook

web = Blueprint("web", __name__)


@web.route("/book/search/<q>/<page>")
def search(q, page):
    # q: 关键字或isbn
    # page: 页数
    print("Test Print")
    print(f"q={q}")
    print(f"page={page}")
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == "isbn":
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)
    return jsonify(result)
    # return json.dumps(result), 200, {"content-type": "application/json"}
