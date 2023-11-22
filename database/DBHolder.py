#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 数据操作对象持有器
    Author  : Lu Li (李露)
    File    : DBHolder.py
    Date    : 2023/11/22 10:37
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from aioredis import Redis

from common.singleton import singleton


@singleton
class DBHolder(object):
    """
    数据操作对象持有器
    """

    __redis = None

    def __init__(self):
        super().__init__()

    @property
    def redis(self) -> Redis:
        return self.__redis

    @redis.setter
    def redis(self, redis: Redis):
        self.__redis = redis


db_holder = DBHolder()
"""数据操作对象持有器单例实例"""
