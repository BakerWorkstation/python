#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import functools

def catchall(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            s = sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
    return wrapped


def log_cost_time(stream):
    def inner_dec(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            import time
            begin = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                print 'func %s cost %s' % (func.__name__, time.time() - begin)
        return wrapped
    return inner_dec

import sys
@catchall
@log_cost_time(sys.stdout)
def complex_func(num):
    ret = 0 ,
    for i in xrange(num):
        ret += i * i
    return ret

#complex_func = log_cost_time(complex_func)

if __name__ == '__main__':
    print complex_func(10000)
    print complex_func.__name__
