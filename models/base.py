# -*- coding:utf-8 -*-
"""
@Time : 2022/4/24 10:40 AM
@Author: binkuolo
@Des: 基础模型
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
