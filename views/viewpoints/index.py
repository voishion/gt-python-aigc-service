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

from config import settings
from core.Nacos import nacos_config
from schemas.index import IndexResp

router = APIRouter()


@router.get("/", summary="门户首页页面", response_class=HTMLResponse)
async def index(request: Request):
    """
    门户首页
    :param request:
    :return:
    """
    resp = IndexResp(
        title=settings.PROJECT_NAME,
        lfasr_app_id=nacos_config.LFASR_APP_ID,
        lfasr_account_id=nacos_config.LFASR_ACCOUNT_ID,
        lfasr_sso_session_id=nacos_config.LFASR_SSO_SESSION_ID
    )
    return request.app.state.views.TemplateResponse("index.html", {"request": request, "resp": resp})
