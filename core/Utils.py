#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 工具函数
    Author  : Lu Li (李露)
    File    : Utils.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

import hashlib
import random
import uuid
from passlib.handlers.pbkdf2 import pbkdf2_sha256


def random_str():
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)


def random_uuid():
    """
    随机生成UUID
    """
    return str(uuid.uuid4()).replace('-', '')


def en_password(psw: str):
    """
    密码加密
    :param psw: 需要加密的密码
    :return: 加密后的密码
    """
    password = pbkdf2_sha256.hash(psw)
    return password


def check_password(password: str, old: str):
    """
    密码校验
    :param password: 用户输入的密码
    :param old: 数据库密码
    :return: Boolean
    """
    check = pbkdf2_sha256.verify(password, old)
    if check:
        return True
    else:
        return False


def code_number(ln: int):
    """
    随机数字
    :param ln: 长度
    :return: str
    """
    code = ""
    for i in range(ln):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch

    return code


def current_time_millis() -> int:
    """
    获取当前时间戳
    :return:
    """
    import time
    return int(time.time() * 1000)
