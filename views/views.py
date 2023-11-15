# -*- coding:utf-8 -*-
"""
@Time : 2022/4/23 11:46 AM
@Author: binkuolo
@Des: 视图路由
"""
from fastapi import APIRouter
from views.viewpoints import index

views_router = APIRouter()

views_router.include_router(index.router, tags=["首页"])

