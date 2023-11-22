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


class MeetingMessageIdReq(BaseModel):
    content: Optional[str] = Field(min_length=1, max_length=999999, description="会议内容")


class MeetingMessageIdResp(BaseResp):
    data: Optional[str] = Field(description="会议总结消息ID")


class MeetingSummaryReq(BaseModel):
    message_id: Optional[str] = Field(min_length=32, max_length=32, description="消息编号")


class MeetingSummaryResp(BaseResp):
    data: Optional[str] = Field(description="会议总结")


class MeetingSummaryStopResp(BaseResp):
    data: Optional[bool] = Field(description="停止结果：true-成功，false-失败")


class LfasrInfo(BaseModel):
    count: Optional[str] = Field(description="套餐时长")
    leftCount: Optional[str] = Field(description="剩余时长")


class LfasrInfoResp(BaseResp):
    data: LfasrInfo
