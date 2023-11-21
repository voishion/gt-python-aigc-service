#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Redis数据库配置
    Author  : Lu Li (李露)
    File    : redis.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

import aioredis
import os
from aioredis import Redis


async def sys_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        f"redis://{os.getenv('CACHE_HOST', '10.152.160.26')}:{os.getenv('CACHE_PORT', 63831)}",
        db=os.getenv('CACHE_DB', 5),
        password=os.getenv('CACHE_PS', 'chen1211'),
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)
