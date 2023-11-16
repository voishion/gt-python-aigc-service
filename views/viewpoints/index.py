#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 首页视图
    Author  : Lu Li (李露)
    File    : index.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", summary="门户首页页面", response_class=HTMLResponse)
async def index(request: Request):
    """
    门户首页
    :param request:
    :return:
    """
    return request.app.state.views.TemplateResponse("index.html", {"request": request})
