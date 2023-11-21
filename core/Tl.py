#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : ThreadLocal集中处理
    Author  : Lu Li (李露)
    File    : Tl.py
    Date    : 2023/11/20 15:36
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from common import const
from config import settings
from core.Plugins import ThreadLocal

# 全链路_idp_session
_x_idp_session = ThreadLocal("x_idp_session", default=settings.PROJECT_NAME)  # _idp_session
# 全链路日志追踪
_x_trace_task_id = ThreadLocal('x_trace_task_id', default=const.CENTER_STROKE_LINE)  # 任务ID
_x_trace_request_id = ThreadLocal("x_trace_request_id", default=const.CENTER_STROKE_LINE)  # 请求ID


def setCurrThreadInfo(**kwargs):
    """
    设置当前线程参数，用于子线程使用
    :param kwargs: req_id:请求ID, task_id:任务ID, idp_session:idp_session
    """
    TraceID.set_req_id(kwargs['req_id'])
    _x_trace_task_id.data = kwargs['task_id']
    IdpSession.set_idp_session(kwargs['idp_session'])


def getCurrThreadInfo() -> dict:
    """
    获取当前线程参数，用于子线程使用
    :return: req_id:请求ID, task_id:任务ID, idp_session:idp_session
    """
    return {
        'req_id': TraceID.get_req_id(),
        'task_id': TraceID.get_task_id(),
        'idp_session': IdpSession.get_idp_session()
    }


class TraceID:
    """全链路追踪ID"""

    @staticmethod
    def set_req_id(req_id: str):
        """
        设置全链路追踪请求ID
        :param req_id: 请求ID
        """
        _x_trace_request_id.data = req_id

    @staticmethod
    def get_req_id() -> str:
        """
        获取全链路追踪请求ID
        :return: 请求ID
        """
        return _x_trace_request_id.data

    @staticmethod
    def set_task_id(task_id: str, task_name: str = "task"):
        """
        设置全链路追踪任务ID，例如:TraceID.set_task_id('A', 'into_summary_sse')
        :param task_id: 任务ID
        :param task_name: 任务名称
        :return: None
        """
        _x_trace_task_id.data = '{}:{}'.format(task_id, task_name)

    @staticmethod
    def get_task_id():
        """
        获取全链路追踪任务ID
        :return: 任务ID
        """
        return _x_trace_task_id.data


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
