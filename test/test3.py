import threading
import time
from werkzeug.local import Local

"""
模拟线程隔离
L是线程隔离的对象
线程t1操作L.a和线程t2操作L.a并不会相互影响

使用线程隔离的意义在于 使当前线程能够正确引用到他自己所创建的对象
而不是引用到其他线程所创建的对象

以线程id号作为key的字典-> Local->LocalStack 都是线程隔离对象
AppContext RequestContext -> LocalStack
Flask -> AppContext Request -> RequestContext
current_app -> LocalStack.top == Appcontext top.app=Flask
request -> LocalStack.top == RequestContext top.request=Request
"""

# 被线程隔离对象
class A:
    b = 1

# 线程隔离对象Local，使用是my_obj操作可以做到线程隔离
my_obj = Local()
my_obj.b = 5


def work():
    my_obj.b = 2
    print("new threading")
    print(my_obj.b)

new_t = threading.Thread(target=work)
new_t.start()

time.sleep(1)
print("main threading")
print(my_obj.b)
