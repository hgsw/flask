import threading
import time
from werkzeug.local import Local

"""
模拟线程隔离
L是线程隔离的对象
线程t1操作L.a和线程t2操作L.a并不会相互影响

使用线程隔离的意义在于 使当前线程能够正确引用到他自己所创建的对象
而不是引用到其他线程所创建的对象

以线程id号作为key的字典-> Local(原理是字典实现)和LocalStack(原理是继承Local)都是线程隔离对象，操作方式不一样
AppContext RequestContext -> LocalStack
Flask -> AppContext Request -> RequestContext
current_app -> LocalStack.top == Appcontext top.app=Flask
request -> LocalStack.top == RequestContext top.request=Request
"""


# 被线程隔离对象
class A:
    b = 1


my_obj = A()
# 主线程修改
my_obj.b = 5


def work():
    # 子线程修改
    my_obj.b = 2
    print("new threading")
    print(my_obj.b)


new_t = threading.Thread(target=work)
new_t.start()

time.sleep(1)
print("main threading")
print(my_obj.b)


print("=" * 50)


# 线程隔离对象
# Local内部正是通过ContextVar与每个线程上下文的绑定，以及对属性访问操作的重定向，
# 使得Local类能够实现在不同线程中调用属性时保持相互独立，即实现了线程隔离。
my_obj = Local()
# 主线程修改
my_obj.b = 5


def work():
    # 子线程修改
    my_obj.b = 2
    print("new threading")
    print(my_obj.b)


new_t = threading.Thread(target=work)
new_t.start()

time.sleep(1)
print("main threading")
print(my_obj.b)
