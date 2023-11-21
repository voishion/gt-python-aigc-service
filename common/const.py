#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 系统常量
    Author  : Lu Li (李露)
    File    : const.py
    Date    : 2023/11/16 14:42
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from config import settings

DATE_FORMAT = "%B %d, %Y"
TIME_FORMAT = "%H:%M"

CHATGLM3_6B = "chatglm3-6b"

SSE_RETRY = 15000

IDP_SESSION = "_idp_session"
DEFAULT_IDP_SESSION = settings.PROJECT_NAME

TASK_ID_KEY = "X-Task-Id"
REQUEST_ID_KEY = "X-Request-Id"

CENTER_STROKE_LINE = "-"
"""中划线"""
