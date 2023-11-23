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

    STOP = '00'
    """停止"""

    NORMAL = '01'
    """正常"""

    def __str__(self):
        return self.name


class NacosConfigType(Enum):
    """
    Nacos配置文件类型，目前仅支持Properties和YAML类型
    """

    PROPERTIES = 'Properties'
    """Properties"""

    YAML = 'YAML'
    """YAML"""

    def __str__(self):
        return self.name


if __name__ == '__main__':
    format_ = [x.value for x in NacosConfigType]
    print('Propertiess' in format_)

