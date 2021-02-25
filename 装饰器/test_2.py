#!/usr/bin/env python
# -*- coding:UTF-8 -*-

def deco(arg):
    def _deco(function):
        def __deco():
            print("addfunction:%s"%arg)
            a = function()
            return a
        return __deco
    return _deco


@deco("hahaha")
def function():
    print("function功能")
    return 2


print function()
