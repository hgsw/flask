from contextlib import contextmanager


# Test 1 ============================================
@contextmanager
def book_mark():
    print("<", end="")
    yield  # 中断当前函数执行，当with语句执行后，在继续执行后面的代码
    print(">", end="")


# with book_mark():
#     print("hello", end="")  # <hello>


# Test 2 ============================================
class Test_with:
    @contextmanager
    def auto_commit(self):
        try:
            yield
            print("代码正常执行完成")
        except Exception as e:
            print("有异常发生做一些事情")
            raise e


db = Test_with()

with db.auto_commit():
    # 这里操作了两张表，需要事务处理，需要回滚
    a = 1
    b = a + 1
    print("job...")
    # c = b / 0  # 制造异常

# Test 3 ============================================
# 子类自动拥有父类的属性
from datetime import datetime


class BaseClass:
    def __init__(self):
        self.timestamp = int(datetime.now().timestamp())

    def a(self):
        pass


class Student(BaseClass):
    age = 18
    name = "Tom"


# student = Student()
# print(student.timestamp)
