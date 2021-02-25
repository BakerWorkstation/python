#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

# @Time    : 2018/5/23 17:51
# @Author  : JY.Liu
# @Site    : http://github.com/lh1993
# @File    : example_6.py
# @Software: PyCharm

#import pysnooper
from datetime import datetime
from decorator import decorate, decorator


def debug(func, *args, **kwargs):
    """print log before a function."""
    print("[DEBUG] {}: enter {}()".format(datetime.now(), func.__name__))
    return func(*args, **kwargs)

def logging1(func):
    return decorate(func, debug)  # way #1

@logging1
def say(something):
    """say something"""
    print("say {}!".format(something))

########################################################################

@decorator
def logging2(func, *args, **kwargs):
    print("[DEBUG] {}: enter {}()".format(datetime.now(), func.__name__))
    return func(*args, **kwargs)

@pysnooper.snoop()
@logging2
def do(work):
    """do work"""
    print("do {}...".format(work))  # way #2

if __name__ == "__main__":
    say("hello word")
    do("hard work")
