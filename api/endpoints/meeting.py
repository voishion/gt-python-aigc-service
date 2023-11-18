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

from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse

from core.Response import success
from schemas import meeting
from service.meeting_service import MeetingService

router = APIRouter(prefix='')


@router.post(
    path='/summary',
    summary="会议总结",
    description="通过人工智能实现文字会议纪要的总结",
    response_model=meeting.MeetingSummaryResp,
)
async def summary(req: Request, post: meeting.MeetingSummaryReq):
    result = MeetingService().meeting_summary(req, post.content)
    return success(msg="会议总结完成", data=result)


@router.get(
    path='/summary-sse',
    summary="会议总结 SSE",
    description="通过人工智能实现文字会议纪要的总结 (SSE)",
)
async def summary_sse(req: Request, content: str = Query(default="你是谁？", min_length=1, description="会议内容")):
    generator = MeetingService().meeting_summary_sse(req, content)
    return StreamingResponse(generator, media_type="text/event-stream")
