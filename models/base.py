#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 基础模型
    Author  : Lu Li (李露)
    File    : base.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""


class User:
    def __init__(self, user_id, user_type, user_scopes):
        self.user_id = user_id
        self.user_type = user_type
        self.user_status = 1
        self.scopes = user_scopes

    def scopes_check(self, scopes):
        """
        权限检查
        :param scopes:
        :return:
        """
        # 去重
        _scopes = set(scopes)
        _self_scopes = set(self.scopes)
        # 对比
        for scope in _scopes:
            if scope not in _self_scopes:
                return False
        return True

    @staticmethod
    def of(user_id, user_type, user_scopes):
        return User(user_id, user_type, user_scopes)
