# -*- coding:utf-8 -*-
"""
@Time : 2022/5/18 1:03 AM
@Author: binkuolo
@Des: 权限管理
"""

from fastapi import Request, APIRouter, Security

from common.enums import Scopes
from core.Auth import check_permissions
from core.Response import fail, success
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
