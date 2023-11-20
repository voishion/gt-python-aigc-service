#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 会议服务
    Author  : Lu Li (李露)
    File    : meeting_service.py
    Date    : 2023/11/16 16:36
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
import time
from datetime import datetime

import openai
from fastapi import Request

from common import const
from common.const import IDP_SESSION
from common.const import DATE_FORMAT, TIME_FORMAT, CHATGLM3_6B
from common.singleton import singleton
from config import settings
from core.Logger import log


@singleton
class MeetingService(object):
    """
    会议服务
    """
    openai.api_base = settings.CHATGLM3_SERVER_URL
    openai.api_key = "any"

    def __init__(self):
        super().__init__()

    def __get_system_prompt(self) -> str:
        return (
            ('You are Smart Xiaotong, the large-model artificial intelligence assistant of General Technology Group. '
             'Today is {}, and the current time is {}, Answer the following questions as best as you can. You have '
             'access to the following tools:')
            .format(datetime.now().strftime(DATE_FORMAT),
                    datetime.now().strftime(TIME_FORMAT)))

    def __get_user_prompt(self, content: str) -> str:
        return ('请将以下文本总结成会议纪要，重点在于会议核心思想以及会议内容，文本中包含说话人姓名和发言时间范围，请使用中文回复，'
                '文本内容如下：\n\n{}').format(content)

    def __get_model_response(self, req: Request, messages, stream=True):
        _idp_session = req.cookies[IDP_SESSION] if IDP_SESSION in req.cookies else const.DEFAULT_IDP_SESSION
        headers = {
            "Authorization": _idp_session,
        }
        params = {
            "model": CHATGLM3_6B,
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.75,
            "top_p": 1,
            "stream": stream,
            "headers": headers
        }
        return openai.ChatCompletion.create(**params)

    def meeting_summary(self, req: Request, content: str) -> str:
        """
        会议总结处理
        :param req: 请求对象
        :param content: 会议内容
        :return: 会议总结
        """
        messages = [
            {"role": "system", "content": self.__get_system_prompt()},
            {"role": "user", "content": self.__get_user_prompt(content)}
        ]
        start_time = time.time()
        try:
            response = self.__get_model_response(req=req, messages=messages, stream=False)
            result = response['choices'][0]['message']['content']
        except Exception as e:
            log.exception("发生异常：%s", str(e))
            result = self.__get_exp_msg(e)
        finally:
            log.debug(f'请求耗时：{time.time() - start_time:.2f} s')
        return result

    def meeting_summary_sse(self, req: Request, content: str):
        """
        会议总结处理，SSE
        :param req: 请求对象
        :param content: 会议内容
        :return: 会议总结推送生成器
        """
        yield "event:initializing\ndata:Initializing...\n\n"

        messages = [
            {"role": "system", "content": self.__get_system_prompt()},
            {"role": "user", "content": self.__get_user_prompt(content)}
        ]
        start_time = time.time()
        # 使用线程池执行API请求
        try:
            response = self.__get_model_response(req=req, messages=messages)
            log.debug(f'请求耗时：{time.time() - start_time:.2f} s')
            for chunk in response:
                delta = chunk.choices[0].delta
                if "content" in delta:
                    _content = delta['content']
                    if _content:
                        yield "data:{}\n\n".format(_content)
                        time.sleep(0.5)
        except Exception as e:
            log.exception("发生异常：%s", str(e))
            yield "data:{}\n\n".format(self.__get_exp_msg(e))

        # 处理完成
        yield "event:completed\ndata:Completed\n\n"
        yield "event:end\ndata:End\n\n"

    def __get_exp_msg(self, e):
        """
        获取异常信息
        :param e:
        :return:
        """
        msg = '网络异常，请稍后再试'
        if isinstance(e, openai.error.APIError):
            if 'API rate limit exceeded' == e.json_body['message']:
                msg = '目前使用人数较多，请稍后再试'
        return msg
