# with 语句异常处理


class MyResourceManager:
    test_lst = ["a", "b", 12]

    def __enter__(self):
        print("Resource is being init...")
        return self

    def __exit__(self, exc_type, exc_value, tb):

        print("Resource is being cleaned up")
        return False

        # 默认返回None，实际上就是False
        # return True   # 不向外抛异常
        # return False  # 默认向外抛异常


#! 当__exit__函数返回值True时，程序正常结束
# with MyResourceManager() as resource:
#     print("Using the resource")
#     1 / 0  # 出现异常，执行with的__exit__函数后退出with，后两行代码不会执行
#     lst = resource.test_lst
#     print(lst)

# print("Test End")


#! 当需要捕获with的异常时__exit__返回值设置False
try:
    with MyResourceManager() as resource:
        print("Using the resource")
        1 / 0
        lst = resource.test_lst
        print(lst)
except Exception as e:
    print(e)  # division by zero

print("Test End")
