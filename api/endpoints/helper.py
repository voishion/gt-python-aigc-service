#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 测试
    Author  : Lu Li (李露)
    File    : helper.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from common.enums import Scopes
from core import Utils
from core.Auth import create_access_token


async def test_oath2(data: OAuth2PasswordRequestForm = Depends()):
    user_type = False
    if not data.scopes:
        raise HTTPException(401, "请选择作用域!")

    if Scopes.IS_ADMIN.value in data.scopes:
        user_type = True
    jwt_data = {
        "user_id": Utils.random_uuid(),
        "user_type": user_type,
        "user_scopes": data.scopes
    }
    jwt_token = create_access_token(data=jwt_data)

    return {"access_token": jwt_token, "token_type": "bearer"}
