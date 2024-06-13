class BookViewModel:
    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.author = book["author"]
        self.pages = book["pages"]
        self.price = book["price"]
        self.summary = book["summary"]
        self.image = book["image"]


class BookCollection:
    def __init__(self):
        self.books = []
        self.total = 0
        self.keyword = ""

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        book = {"books": [], "total": 0, "keyword": keyword}
        if data:
            book["total"] = 1
            book["books"] = [cls._cut_book_data(data)]

        return book

    @classmethod
    def package_collection(cls, data, keyword):
        book = {"books": [], "total": 0, "keyword": keyword}
        if data:
            book["total"] = len(data["books"])
            book["books"] = [cls._cut_book_data(b) for b in data["books"]]

        return book

    @classmethod
    def _cut_book_data(cls, data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "author": data["author"],
            "pages": data["pages"],
            "price": data["price"],
            "summary": data["summary"] or "",
            "image": data["image"] or "",
        }
        return book
