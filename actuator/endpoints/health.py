#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 健康检查探针接口
    Author  : Lu Li (李露)
    File    : health.py
    Date    : 2023/11/18 16:10
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(prefix='')


@router.get("/liveness", description="健康探针", response_class=JSONResponse)
def liveness():
    return {"status": "OK"}


@router.get("/readiness", description="就绪探针", response_class=JSONResponse)
def readiness():
    # 添加逻辑以检查应用程序是否准备好接受流量
    # 如果准备就绪，返回 {"status": "OK"}
    # 否则返回 {"status": "Not Ready"}
    return {"status": "OK"}
