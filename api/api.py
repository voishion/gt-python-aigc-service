# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: api路由
"""
from fastapi import APIRouter
from api.endpoints.helper import test_oath2, apply_temp_token
from api.endpoints import meeting

api_router = APIRouter(prefix="/api/v1")
api_router.post("/test/oath2", tags=["测试oath2授权"])(test_oath2)
api_router.post("/temp/oath2", tags=["申请临时授权"])(apply_temp_token)
api_router.include_router(meeting.router, prefix='/meeting', tags=["会议处理"])

