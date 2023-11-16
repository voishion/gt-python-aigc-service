#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 路由聚合
    Author  : Lu Li (李露)
    File    : Router.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from api.api import api_router
from views.views import views_router
from fastapi import APIRouter


router = APIRouter()
# 视图路由
router.include_router(views_router)
# API路由
router.include_router(api_router)

