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

from common.const import DATE_FORMAT, TIME_FORMAT, CHATGLM3_6B
from common.singleton import singleton
from config import settings

from loguru import logger as log


@singleton
class MeetingService(object):
    """
    会议服务
    """
    openai.api_base = settings.CHATGLM3_SERVER_URL
    openai.api_key = "any"

    def __init__(self):
        super().__init__()

    def meeting_summary(self, content: str) -> str:
        """
        会议总结处理
        :param content: 会议内容
        :return: 会议总结
        """
        content = ('请将以下文本内容转换为会议纪要，需要总结会议核心思想与会后的工作内容，文本内容中包含说话人名字和说话起始范围，'
                   '文本内容如下：\n{}').format(content)
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model=CHATGLM3_6B,
            messages=[
                {"role": "system",
                 "content": f"You are Smart Xiaotong, the large-model artificial intelligence assistant of General "
                            f"Technology Group. Today is {datetime.now().strftime(DATE_FORMAT)}, and the current "
                            f"time is {datetime.now().strftime(TIME_FORMAT)}, Answer the following questions as best "
                            f"as you can. You have access to the following tools:"},
                {"role": "user", "content": content}
            ],
            max_tokens=2048,
            temperature=0.75,
            top_p=1
            # stream=True
        )
        response_time = time.time()
        result = response['choices'][0]['message']['content']
        log.debug(f'请求耗时：{response_time - start_time:.2f} s, result：{result}')
        return result
