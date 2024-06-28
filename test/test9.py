import threading
import time
from werkzeug.local import LocalStack

# LocalStack的stack的特性
# my_obj = LocalStack()
# my_obj.push(1)
# my_obj.push(2)
# my_obj.push({"id": 1234, "name": "to"})

# print(my_obj.pop().get("id"))
# print(my_obj.top)  # None 没有就是None
# print(my_obj.pop())
# print(my_obj.pop())

# LocalStack的local的特性
my_obj = LocalStack()
my_obj.push(1)
print(f"main threading top={my_obj.top}")


def work():
    print(f"sub threading top={my_obj.top}")
    my_obj.push(2)
    print(f"sub threading new push, top={my_obj.top}")


new_t = threading.Thread(target=work)
new_t.start()

time.sleep(1)
# 线程间访问操作my_obj是互相高隔离的
print(f"main threading end top={my_obj.top}")
print("main threading end")
