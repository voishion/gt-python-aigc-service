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
import asyncio
from typing import Callable

from fastapi import FastAPI

from config import settings
from core.Exts import openaiThreadPool
from core.Logger import log
from core.Nacos import nacos_event_listener
from database.DBHolder import db_holder
from database.redis import sys_cache


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        log.info("RUN_ENV:{}", settings.RUN_ENV)
        log.info("{}已启动", settings.PROJECT_NAME)
        # 注册数据库
        # await register_mysql(app)
        db_holder().redis = await sys_cache()
        app.state.openai_thread_pool = await openaiThreadPool()
        # Nacos事件监听
        asyncio.create_task(nacos_event_listener())
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
        cache = db_holder().redis
        await cache.close()

    return stop_app
