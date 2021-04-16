#如果我们需要记录部分函数的执行时间，函数执行前后打印一些日志，装饰器是一种很方便的选择

#代码如下：

import time
import functools
 
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'函数 {func.__name__} 耗时 {(end - start) * 1000} ms')
        return res
    return wrapper
#装饰器 log 记录某个函数的运行时间，并返回其执行结果

#测试一下：

@log
def now():
    print('2021-7-1')
    
now()
#结果：

#2021-7-1
#函数 now 耗时 0.09933599994838005 ms
