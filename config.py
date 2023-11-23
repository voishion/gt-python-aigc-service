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
import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

from common.enums import NacosConfigType


class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(".env.{}".format(os.getenv("RUN_ENV", "test"))), override=True)
    # 运行环境
    RUN_ENV: str = os.getenv("RUN_ENV", "test")
    # 日志打印级别
    LOG_PATH: str = "logs"
    # 日志打印级别，DEBUG、INFO、WARNING、ERROR、CRITICAL
    LOG_LEVEL: str = "DEBUG"
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
    SECRET_KEY: str = "eb3e38720c7a432fab6f1126b97a968e"
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

    # Nacos连接地址
    NACOS_SERVER_ADDRESSES: str = "localhost:8848"
    # Nacos命名空间
    NACOS_NAMESPACE: str = "public"
    # Nacos用户名
    NACOS_USERNAME: str = 'nacos'
    # Nacos密码
    NACOS_PASSWORD: str = 'nacos'
    # Nacos分组
    NACOS_GROUP: str = "DEFAULT_GROUP"
    # Nacos数据编号
    NACOS_DATA_ID: str = PROJECT_NAME
    # Nacos配置文件格式
    NACOS_CONFIG_TYPE: str = NacosConfigType.PROPERTIES.value


settings = Config()
