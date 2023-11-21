#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Redis缓存键组装
    Author  : Lu Li (李露)
    File    : redis_key.py
    Date    : 2023/11/21 17:10
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from typing import Awaitable

from fastapi import Request

from common.const import REDIS_CACHE_ROOT_KEY


class RedisService:
    """Redis服务"""

    @staticmethod
    def set(req: Request, key: str, value, expire_seconds: int) -> Awaitable:
        """
        设置缓存
        :param req: 请求对象
        :param key: 缓存键
        :param value: 缓存值
        :param expire_seconds: 过期时间，秒
        :return:
        """
        return req.app.state.cache.set(name=key, value=value, ex=expire_seconds)


class RedisKey:
    """Redis键处理"""

    @staticmethod
    def message_id_key(message_id) -> str:
        return '{}:message_id:{}'.format(REDIS_CACHE_ROOT_KEY, message_id)
