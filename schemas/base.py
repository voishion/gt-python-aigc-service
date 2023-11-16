#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 基础schemas
    Author  : Lu Li (李露)
    File    : base.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from pydantic import BaseModel, Field
from typing import List


class BaseResp(BaseModel):
    code: int = Field(description="状态码")
    message: str = Field(description="信息")
    data: List = Field(description="数据")
