#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 会议处理
    Author  : Lu Li (李露)
    File    : meeting.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

from fastapi import Request, APIRouter, Security

from common.enums import Scopes
from core.Auth import check_permissions
from core.Response import success
from schemas import meeting

router = APIRouter(prefix='')


@router.post('/summary', response_model=meeting.MeetingSummaryResp, summary="会议总结",
             dependencies=[Security(check_permissions, scopes=[Scopes.ACCESS_API.value])])
async def summary(req: Request, post: meeting.MeetingSummaryReq):
    """
    创建权限
    :param req:
    :param post: CreateAccess
    :return:
    """
    print(req)
    print(post)
    return success(msg="会议总结完成", data="会议圆满成功")
