# -*- coding:utf-8 -*-
"""
@Time : 2022/5/5 1:30 AM
@Author: binkuolo
@Des: 测试
"""
from fastapi import Depends, HTTPException
from fastapi import Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from core import Utils
from core.Auth import create_access_token


async def test_oath2(data: OAuth2PasswordRequestForm = Depends()):
    user_type = False
    if not data.scopes:
        raise HTTPException(401, "请选择作用域!")
    if "is_admin" in data.scopes:
        user_type = True
    jwt_data = {
        "user_id": data.client_id,
        "user_type": user_type
    }
    jwt_token = create_access_token(data=jwt_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


async def apply_temp_token(request: Request):
    """
    apply_temp_token
    :param request:
    :return:
    """
    jwt_data = {
        "user_id": Utils.random_uuid(),
        "user_type": '1'
    }
    jwt_token = create_access_token(data=jwt_data)
    return {"access_token": jwt_token, "token_type": "bearer"}
