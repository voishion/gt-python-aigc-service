#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Api路由
    Author  : Lu Li (李露)
    File    : api.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from fastapi import APIRouter

from api.endpoints import meeting
from api.endpoints.helper import test_oath2

api_router = APIRouter(prefix="/api/v1")
api_router.post("/test/oath2", tags=["测试oath2授权"])(test_oath2)
api_router.include_router(meeting.router, prefix='/meeting', tags=["会议处理"])

