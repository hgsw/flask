"""  python 是不能序列化一个对象，但是可以序列化一个字典
我们需要将一个对象转化为字典 """

import json


class Book:

    def __init__(self):
        self.total = 1
        self.books = ["hello"]

    def add_book(self, book_name):
        self.books.append(book_name)


book = Book()
# print(json.dumps(book))
# 对象不能序列化 TypeError: Object of type Book is not JSON serializable

book.add_book("world")
# print(json.dumps(book.__dict__))
# {"total": 1, "books": ["hello", "world"]}


class BookSet:
    def __init__(self):
        self.total = 1
        self.bookset = []

    def add_book(self, book):
        self.bookset.append(book)


books = BookSet()
books.add_book(book)

# print(json.dumps(books.__dict__))
# 直接序列化报错 TypeError: Object of type Book is not JSON serializable

# 序列化一个对象时，其属性也是对象的话，需要先将对象序列化字典
# 此时需要default参数传入一个函数告诉dumps如何处理不能序列化的属性
print(json.dumps(books, default=lambda o: o.__dict__))
# {"total": 1, "bookset": [{"total": 1, "books": ["hello", "world"]}]}
