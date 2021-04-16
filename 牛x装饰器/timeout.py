'''
任务超时退出

我们日常在使用的各种网络请求库时都带有 timeout 参数，例如：request 库

这个参数可以使请求超时就不再继续了，直接抛出超时错误，避免等太久

如果我们自己开发的方法也希望增加这个功能，该如何做呢？

方法很多，但最简单直接的是使用并发库 futures，为了使用方便，我将其封装成了一个装饰器，代码如下：
'''

import functools
from concurrent import futures

executor = futures.ThreadPoolExecutor(1)

def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            future = executor.submit(func, *args, **kw)
            return future.result(timeout=seconds)
        return wrapper
    return decorator

#定义了以上函数，我们就有了一个超时结束的装饰器，下面可以测试一下：

import time

@timeout(1)
def task(a, b):
    time.sleep(1.2)
    return a+b

task(2, 3)
'''
结果：

---------------------------------------------------------------------------
TimeoutError                              Traceback (most recent call last)
...
D:\Anaconda3\lib\concurrent\futures\_base.py in result(self, timeout)
    432                 return self.__get_result()
    433             else:
--> 434                 raise TimeoutError()
    435 
    436     def exception(self, timeout=None):

TimeoutError:
上面我们通过装饰器定义了函数的超时时间为 1 秒，通过睡眠模拟函数执行超过 1 秒时，成功的抛出了超时异常
'''

#程序能够在超时时间内完成时：

@timeout(1)
def task(a, b):
    time.sleep(0.9)
    return a+b

task(2, 3)
'''
结果：

5
可以看到，顺利的得到了结果

这样我们就可以通过一个装饰器给任何函数增加超时时间，这个函数在规定时间内还处理不完就可以直接结束任务

前面我将这个装饰器将所需的变量定义到了外部，其实我们还可以通过类装饰器进一步封装，代码如下：
'''

import functools
from concurrent import futures

class timeout:
    __executor = futures.ThreadPoolExecutor(1)

    def __init__(self, seconds):
        self.seconds = seconds

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            future = timeout.__executor.submit(func, *args, **kw)
            return future.result(timeout=self.seconds)
        return wrapper
'''
经测试使用类装饰器能得到同样的效果。

注意：使用 @functools.wraps 的目的是因为被装饰的 func 函数元信息会被替换为 wrapper 函数的元信息，而 @functools.wraps(func) 将 wrapper 函数的元信息替换为 func 函数的元信息。最终虽然返回的是 wrapper 函数，元信息却依然是原有的 func 函数
在函数式编程中，函数的返回值是函数对象被称为闭包
'''
