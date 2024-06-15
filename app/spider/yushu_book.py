from app.libs.http2 import HTTP
from flask import current_app
from app.models.book import Book


class YuShuBook:
    """如果一个类只有方法而没有属性，本质上还是面向过程的思想
    不需要保存查询的过程变量，关注类本身的功能，不需要过分具体（保持一定的抽象化）

    当有一天修改了book获取的来源，我们是不用过分关心其获取的具体参数，所以我们是不需要记录
    过多的中间变量"""

    # isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"
    isbn_url = "http://api.tanshuapi.com/api/isbn/v1/index?key={}&isbn={}"

    def __init__(self):
        self.total = 0
        # 保存书籍获取的原始数据
        self.books = []

    def search_by_isbn(self, isbn):
        """isbn查询数据，返回一个"""
        # 获取三方api接口的token
        # key = current_app.config["KEY"]

        # url = self.isbn_url.format(key, isbn)
        # result = HTTP.get(url)

        # 数据库查询方式
        result = Book.query.filter_by(isbn=isbn).first()
        if result:
            result = {
                "id": result.id,
                "title": result.title,
                "author": result.author,
                "binging": result.binging,
                "publisher": result.publisher,
                "price": result.price,
                "pages": result.pages,
                "pubdate": result.pubdate,
                "isbn": result.isbn,
                "summary": result.summary,
                "image": result.image,
            }
            self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        """根据关键词查询书籍，可以返回多个数据"""
        url = self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.calculate_start(page))
        result = HTTP.get(url)
        return result

    def calculate_start(self, page):
        """
        函数封装的优势
        1、功能简洁，提高复用性
        2、函数名自带解释性
        """
        return (page - 1) * current_app.config["PER_PAGE"]

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        # 关键字查询，会返回多个books的结果
        self.total = data["pages"]
        self.books.append(data["books"])
