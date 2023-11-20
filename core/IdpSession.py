#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : _idp_session处理
    Author  : Lu Li (李露)
    File    : IdpSession.py
    Date    : 2023/11/20 15:36
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

from config import settings
from core.ThreadLocal import ThreadLocal

# 全链路_idp_session
_x_idp_session = ThreadLocal("x_idp_session", default=settings.PROJECT_NAME)  # _idp_session


class IdpSession:
    """
    全链路_idp_session处理
    """

    @staticmethod
    def set_idp_session(idp_session: str):
        """
        设置全链路_idp_session
        :param idp_session: _idp_session
        :return: None
        """
        _x_idp_session.data = idp_session

    @staticmethod
    def get_idp_session() -> str:
        """
        获取全链路_idp_session
        :return: _idp_session
        """
        return _x_idp_session.data
