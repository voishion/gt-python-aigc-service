#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 首页schemas模型
    Author  : Lu Li (李露)
    File    : index.py
    Date    : 2023/11/16 14:06
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from typing import Optional

from pydantic import Field, BaseModel


class IndexResp(BaseModel):
    title: Optional[str] = Field(default=None, description="主题")
    lfasr_app_id: Optional[str] = Field(default=None, description="科大讯飞_语音转写_APPID")
    lfasr_account_id: Optional[str] = Field(default=None, description="科大讯飞_语音转写_ACCOUNT_ID")
    lfasr_sso_session_id: Optional[str] = Field(default=None, description="科大讯飞_语音转写_SSO_SESSION_ID")
