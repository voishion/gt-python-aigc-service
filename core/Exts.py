#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 说明
    Author  : Lu Li (李露)
    File    : Exts.py
    Date    : 2023/11/18 13:00
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from concurrent.futures import ThreadPoolExecutor


async def openaiThreadPool() -> ThreadPoolExecutor:
    # 创建一个线程池执行器
    return ThreadPoolExecutor(max_workers=4, thread_name_prefix="openaiThreadPool")
