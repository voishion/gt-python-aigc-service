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

from actuator.endpoints import health

actuator_router = APIRouter(prefix="/actuator")
actuator_router.include_router(health.router, prefix='/health', tags=["Kubernetes探针"])

