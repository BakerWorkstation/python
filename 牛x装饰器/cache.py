'''
缓存

如果经常调用一个函数，而且参数经常会产生重复，如果把结果缓存起来，下次调用同样参数时就会节省处理时间

定义函数：
'''
import math
import random
import time


def task(x):
    time.sleep(0.01)
    return round(math.log(x**3 / 15), 4)
#执行：

%%time
for i in range(500):
    task(random.randrange(5, 10))
#结果：

#Wall time: 5.01 s
#此时如果我们使用缓存的效果就会大不一样，实现缓存的装饰器有很多，我就不重复造轮子了，这里使用 functools 包下的 LRU 缓存：

from functools import lru_cache

@lru_cache()
def task(x):
    time.sleep(0.01)
    return round(math.log(x**3 / 15), 4)
#执行：

%%time
for i in range(500):
    task(random.randrange(5, 10))
#结果：

#Wall time: 50 ms
