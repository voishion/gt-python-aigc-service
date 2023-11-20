#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : ThreadLocal
    Author  : Lu Li (李露)
    File    : ThreadLocal.py
    Date    : 2023/11/20 17:12
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
import threading


class ThreadLocal(threading.local):
    def __init__(self, name, *args, **kwargs):
        self.__data = None
        self.__name = name
        if 'default' in kwargs:
            self.__default = kwargs['default']

    @property
    def data(self):
        if self.__data:
            return self.__data
        else:
            if self.__default:
                return self.__default
            else:
                return None

    @data.setter
    def data(self, value):
        self.__data = value

    def __str__(self):
        return f"自定义ThreadLocal, name:{self.__name}, data:{self.__data}, default:{self.__default}"
