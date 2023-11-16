#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 单例装饰器
    Author  : Lu Li (李露)
    File    : singleton.py
    Date    : 2023/11/16 17:08
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""


def singleton(cls):
    """
    单例装饰器
    :param cls:
    :return:
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
