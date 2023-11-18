#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 日志配置
    Author  : Lu Li (李露)
    File    : Logger.py
    Date    : 2023/11/18 18:58
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

'''
    # <red>: 红色
    # <green>: 绿色
    # <yellow>: 黄色
    # <blue>: 蓝色
    # <magenta>: 品红色
    # <cyan>: 青色
    # <white>: 白色
    # <black>: 黑色
    # rotation="00:00" 每日更新时间，rotation="12:00"，rotation="1 week"，rotation="5kb"
'''
import os
import sys
import time
import logging
from types import FrameType
from typing import cast
from loguru import logger

from config import settings

__all__ = ["log", "Loggers"]

# 不记录日志的日志名称
EXCLUDE_LOG_NAME = {
    'uvicorn.protocols.http.httptools_impl'
}


class Logger:
    """输出日志到文件和控制台"""

    def __filter(self, record):
        return record["name"] not in EXCLUDE_LOG_NAME

    def __init__(self):
        # 文件的命名
        log_name = f"Fast_{time.strftime('%Y-%m-%d', time.localtime()).replace('-', '_')}.log"
        log_path = os.path.join(settings.LOG_PATH, log_name)
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 判断日志文件夹是否存在，不存则创建
        if not os.path.exists(settings.LOG_PATH):
            os.makedirs(settings.LOG_PATH)
        # 日志输出格式
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout,
                        format="<green>{time:YYYY-MM-DD HH:mm:ss.ms}</green> | "
                               "<level>{level:<8}</level> | "
                               "<yellow>{process:<5}</yellow> | "
                               "<magenta>{thread:<15}</magenta> | "
                               "<cyan>{name}:{function}</cyan>:<cyan><level>{line}</level></cyan> - "
                               "<level>{message}</level>",
                        filter=self.__filter,
                        level=settings.LOG_LEVEL)
        # 日志写入文件
        self.logger.add(log_path,
                        format='{time:YYYY-MM-DD HH:mm:ss.ms} | '
                               "{level:<8} | "
                               "{process} | "
                               "{thread} | "
                               '{name}:{function}:{line} - {message}',
                        encoding='utf-8',
                        retention='7 days',  # 设置历史保留时长
                        backtrace=True,  # 回溯
                        diagnose=True,  # 诊断
                        enqueue=True,  # 异步写入
                        rotation="00:00",  # 每日更新时间
                        # filter="my_module",  # 过滤模块
                        compression="zip",  # 文件压缩
                        level=settings.LOG_LEVEL)

    def init_config(self):
        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

        # change handler for default uvicorn logger
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]

    def get_logger(self):
        return self.logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


Loggers = Logger()
log = Loggers.get_logger()
