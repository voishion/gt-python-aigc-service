#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 基本配置文件
    Author  : Lu Li (李露)
    File    : config.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
import logging
import os
from dotenv import load_dotenv, find_dotenv
from typing import List

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)
    # 日志打印级别
    LOG_LEVEL: int = logging.INFO
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "gt-python-aigc-service"
    DESCRIPTION: str = '<a href="/redoc" target="_blank">redoc</a>'
    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    TEMPLATE_DIR: str = os.path.join(os.getcwd(), "templates")
    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]
    # Session
    SECRET_KEY: str = "session"
    SESSION_COOKIE: str = "session_id"
    SESSION_MAX_AGE: int = 14 * 24 * 60 * 60
    # Jwt
    JWT_SECRET_KEY: str = "01d35e094faa6cm2556c818166b7v4563b93f7099f0f0f4caa6cf63b86e8d3e0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60

    SWAGGER_UI_OAUTH2_REDIRECT_URL: str = "/api/v1/test/oath2"

    # CHATGLM3地址
    CHATGLM3_SERVER_URL: str = "https://esb.gt.cn/v1"
    # 天气接口KEY
    SENIVERSE_KEY: str = "Sp-dfPkJHO8lvb055"


settings = Config()
