#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 新闻相关schemas模型
    Author  : Lu Li (李露)
    File    : news.py
    Date    : 2023/11/16 14:06
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from typing import Optional

from pydantic import Field, BaseModel

from schemas.base import BaseResp


class NewsSearchReq(BaseModel):
    prompt: Optional[str] = Field(min_length=1, max_length=50, description="搜索提示词")


class NewsSearchResp(BaseResp):
    data: Optional[str] = Field(description="搜索结果")
