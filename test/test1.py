"""
线程是进程的一部分
进程的粒度太大，进程之间的切换代价较大

系统进行资源分配的基本单位 如内存、网络等
系统能够进行任务调度的最小单位(通俗理解是利用cpu执行代码)
线程自己不拥有资源，但是可以访问进程的资源

多线程核心：更加充分利用多核cpu性能优势

CIL锁 会让Python在任何时刻只能有一个线程在执行，无关cpu核数
单核cpu同一时间只有一个线程在执行代码，多核cpu可以让主线程在一个核上运行，线程在其他核上执行
io密集型任务（如网络请求、数据库查询、文件读写），多线程仍然可以提升效率，因为线程在等待io时会释放GIL，让其他线程有机会执行。
cpu密集型任务 python无法充分利用多核cpu优势
"""

import threading
import time


def work():
    print("a threading")
    # sleep 函数让出cpu，但不会释放该线程持有的其他资源，比如锁、文件句柄等
    time.sleep(10)
    t = threading.current_thread()
    print(t.getName())


new_t = threading.Thread(target=work)
new_t.start()
# 下面代码会很快执行，不会阻塞10s后执行
t = threading.current_thread()
print(t.getName())

print("MainThread is working...")
