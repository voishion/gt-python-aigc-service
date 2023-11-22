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
    :return: 时间戳，如：1700448538223
    """
    import time
    return int(time.time() * 1000)


def uuid4() -> str:
    """
    生成UUID字符串
    :return: UUID，如：d31138db-bd29-46cc-83f7-6c239602bae4
    """
    return str(uuid.uuid4())


def simple_uuid4() -> str:
    """
    生成简单的UUID字符串
    :return: UUID，如：dd318b1b11ab4e7f9fd68b73b7799446
    """
    return uuid4().replace('-', '')


def convert_hours_to_hms(hours):
    """
    将传入的小时数转换为友好的时分秒格式
    :param hours: 小时数，如：3.99754841
    :return: 时分秒，如：03时59分51秒
    """
    total_seconds = int(hours * 3600)
    h, remainder = divmod(total_seconds, 3600)
    m, s = divmod(remainder, 60)
    return "{:02}时{:02}分{:02}秒".format(h, m, s)
