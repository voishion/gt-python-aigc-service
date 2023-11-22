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
    async def set(req: Request, key: str, value, expire_seconds: int) -> Awaitable:
        """
        设置缓存
        :param req: 请求对象
        :param key: 缓存键
        :param value: 缓存值
        :param expire_seconds: 过期时间，秒
        :return:
        """
        return await req.app.state.cache.set(name=key, value=value, ex=expire_seconds)


class RedisKey:
    """Redis键处理"""

    @classmethod
    def message_status(cls, message_id):
        return '{}:message_status:{}'.format(REDIS_CACHE_ROOT_KEY, message_id)

    @classmethod
    def message_content(cls, message_id):
        return '{}:message_content:{}'.format(REDIS_CACHE_ROOT_KEY, message_id)
