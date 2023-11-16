#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 视图路由
    Author  : Lu Li (李露)
    File    : index.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from fastapi import APIRouter
from views.viewpoints import index

views_router = APIRouter()

views_router.include_router(index.router, tags=["首页"])

