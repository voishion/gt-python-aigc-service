#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 枚举信息
    Author  : Lu Li (李露)
    File    : enums.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from enum import Enum


class Scopes(Enum):
    """
    权限范围枚举
    """
    IS_ADMIN = 'is_admin'
    ACCESS_API = 'access_api'
    ACCESS_PAGE = 'access_page'
    ACCESS_TEST = 'access_test'

    def __str__(self):
        return self.name


class MessageStatus(Enum):
    """
    消息状态
    """

    STOP = 0
    """停止"""

    NORMAL = 1
    """正常"""

    def __str__(self):
        return self.name

if __name__ == '__main__':
    print(MessageStatus.NORMAL.value)