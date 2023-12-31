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
from typing import Optional

import requests
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from core import Utils
from core.Nacos import nacos_config
from core.Response import success
from schemas import meeting
from service.meeting_service import meeting_service

router = APIRouter(prefix='')


@router.post(
    path='/message-id',
    summary="会议总结消息ID",
    description="上送会议内容获取会议总结消息ID",
    response_model=meeting.MeetingMessageIdResp,
)
async def message_id(post: meeting.MeetingMessageIdReq):
    result = await meeting_service().message_id(post.content)
    return success(msg="会议总结消息ID生成完成", data=result)


@router.post(
    path='/summary',
    summary="会议总结",
    description="通过人工智能实现文字会议纪要的总结",
    response_model=meeting.MeetingSummaryResp,
)
async def summary(post: meeting.MeetingSummaryReq):
    result = await meeting_service().meeting_summary(post.message_id)
    return success(msg="会议总结完成", data=result)


@router.get(
    path='/summary-sse',
    summary="会议总结 SSE",
    description="通过人工智能实现文字会议纪要的总结 (SSE)",
)
async def summary_sse(message_id: Optional[str] = Query(min_length=32, max_length=32, description="消息编号")):
    generator = meeting_service().meeting_summary_sse(message_id)
    return StreamingResponse(generator, media_type="text/event-stream")


@router.post(
    path='/summary-sse-stop',
    summary="停止会议总结",
    description="停止通过人工智能实现文字会议纪要的总结",
    response_model=meeting.MeetingSummaryStopResp,
)
async def summary(post: meeting.MeetingSummaryReq):
    result = await meeting_service().meeting_summary_sse_stop(post.message_id)
    return success(msg="会议总结停止操作完成", data=result)


@router.get(
    path='/lfasr-info',
    summary="语音转写当前套餐详情",
    description="获取科大讯飞语音转写当前套餐详情",
    response_model=meeting.LfasrInfoResp,
)
async def lfasr_info(
        appId: Optional[str] = Query(default=None, description="appId"),
        account_id: Optional[str] = Query(default=None, description="account_id"),
        ssoSessionId: Optional[str] = Query(default=None, description="ssoSessionId"),
):
    if not appId:
        appId = nacos_config.LFASR_APP_ID
    if not account_id:
        account_id = nacos_config.LFASR_ACCOUNT_ID
    if not ssoSessionId:
        ssoSessionId = nacos_config.LFASR_SSO_SESSION_ID
    headers = {
        "Cookie": "ssoSessionId={}; account_id={};".format(ssoSessionId, account_id),
    }
    url = "https://console.xfyun.cn/dashboard/lfasr/getlfasrInfo?appId={}".format(appId)
    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    data_info = resp.json()['data'][0]
    result = {
        'count': Utils.convert_hours_to_hms(data_info['count']),
        'leftCount': Utils.convert_hours_to_hms(data_info['leftCount'])
    }

    return success(msg="查询完成", data=result)
