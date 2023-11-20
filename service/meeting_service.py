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

from core import Utils
from core.Logger import log

from common.const import DATE_FORMAT, TIME_FORMAT, CHATGLM3_6B
from common.singleton import singleton
from config import settings


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
        headers = {
            "Authorization": "MTAuNDIuNC4w%7CMGE3YmJhZjg4NThiOTVjNTcyMDNjMDg5YmYxYmFjZWJmYWFmNTVkMTA4YzdjNzc3OTRlMDUxZjE2ODY1ZjNiNg%3D%3D%7CpOXzn%2BC1SkAjYrLYDzuCadfIloY%3D",
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
        response = self.__get_model_response(req=req, messages=messages, stream=False)
        log.debug(f'请求耗时：{time.time() - start_time:.2f} s')
        return response['choices'][0]['message']['content']

    def meeting_summary_sse(self, req: Request, content: str):
        """
        会议总结处理，SSE
        :param req: 请求对象
        :param content: 会议内容
        :return: 会议总结推送生成器
        """
        yield "data:\neventTime:{}\n\n".format(Utils.current_time_millis())

        messages = [
            {"role": "system", "content": self.__get_system_prompt()},
            {"role": "user", "content": self.__get_user_prompt(content)}
        ]
        start_time = time.time()
        # 使用线程池执行API请求
        response = self.__get_model_response(req=req, messages=messages)
        log.debug(f'请求耗时：{time.time() - start_time:.2f} s')
        for chunk in response:
            delta = chunk.choices[0].delta
            if "content" in delta:
                _content = delta['content']
                if _content:
                    yield "data:{}\neventTime:{}\n\n".format(_content, Utils.current_time_millis())
                    time.sleep(0.5)

        yield "data:\n\n"
        yield "event:end\nid:stop\ndata:END\neventTime:{}\n\n".format(Utils.current_time_millis())
