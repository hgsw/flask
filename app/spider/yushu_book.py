from app.libs.http2 import HTTP
from flask import current_app


class YuShuBook:
    # isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"
    isbn_url = "http://api.tanshuapi.com/api/isbn/v1/index?key={}&isbn={}"

    @classmethod
    def search_by_isbn(cls, isbn):
        key = current_app.config["KEY"]
        url = cls.isbn_url.format(key, isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        # print("Test Print")
        # print(f"page={page}")
        # print(f"cls.calculate_start(page)={cls.calculate_start(page)}")
        url = cls.keyword_url.format(keyword, current_app.config["PER_PAGE"], cls.calculate_start(page))
        result = HTTP.get(url)
        return result

    @classmethod
    def calculate_start(page):
        """函数封装的优势 1）功能简洁，提高复用性。2）函数名自带解释性"""
        return (page - 1) * current_app.config["PER_PAGE"]
