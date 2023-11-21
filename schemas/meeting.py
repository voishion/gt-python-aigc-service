#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 会议相关schemas模型
    Author  : Lu Li (李露)
    File    : meeting.py
    Date    : 2023/11/16 14:06
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from typing import Optional

from pydantic import Field, BaseModel

from schemas.base import BaseResp


class MeetingMessageIdResp(BaseResp):
    data: Optional[str] = Field(description="会议总结消息ID")


class MeetingSummaryReq(BaseModel):
    content: Optional[str] = Field(min_length=1, max_length=999999, description="会议内容")


class MeetingSummaryResp(BaseResp):
    data: Optional[str] = Field(description="会议总结")
