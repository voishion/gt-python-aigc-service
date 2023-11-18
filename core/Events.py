#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : FastAPI事件监听
    Author  : Lu Li (李露)
    File    : Events.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from typing import Callable

from fastapi import FastAPI

from config import settings
from core.Exts import openaiThreadPool
from core.Logger import log


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        log.info("{}已启动", settings.PROJECT_NAME)
        # 注册数据库
        # await register_mysql(app)
        # 注入缓存到app state
        # app.state.cache = await sys_cache()
        # app.state.code_cache = await code_cache()
        app.state.openai_thread_pool = await openaiThreadPool()

        pass

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        log.info("{}已停止", settings.PROJECT_NAME)
        # cache: Redis = await app.state.cache
        # code: Redis = await app.state.code_cache
        # await cache.close()
        # await code.close()

    return stop_app
