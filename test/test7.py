# 在Python中，当一个类实现了__call__方法，这个类的实例就变成了可调用的对象，也就是说你可以像函数一样直接使用这个类的实例。
# 这样设计的主要目的是为了实现对象的函数式编程风格，或者创建一些类似装饰器、函数对象等场景。
# 具体来说，当你对一个实现了__call__方法的类的实例进行调用操作时（即使用圆括号()），Python会自动调用该实例的__call__方法。
# 这为类的实例提供了一种灵活的调用方式，并且可以在调用时传递参数，就像调用普通函数一样。


class CallableClass:

    def __init__(self, message):
        self.message = message

    def __call__(self, name):
        print(f"{self.message}, {name}!")


callable_instance = CallableClass("Hello")

# 直接像函数那样调用这个实例
callable_instance("World")
# Hello, World!
