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
import asyncio
import time
from datetime import datetime

import openai
from starlette import status
from starlette.exceptions import HTTPException

from common.const import DATE_FORMAT, TIME_FORMAT, CHATGLM3_6B
from common.enums import MessageStatus
from common.singleton import singleton
from config import settings
from core import Utils
from core.Logger import log
from core.RedisHelper import RedisKey, RedisService
from core.Tl import IdpSession


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
        return ('你是通用科技集团的大模人工智能助手智慧小通。 今天是{}，当前时间是{}，请尽可能使用中文回答以下问题：'
                .format(datetime.now().strftime(DATE_FORMAT), datetime.now().strftime(TIME_FORMAT)))

    def __get_user_prompt(self, content: str) -> str:
        return ('请将以下文本总结成会议纪要，重点在于会议核心思想以及会议内容，文本中包含说话人姓名和发言时间范围，'
                '文本内容如下：\n\n{}').format(content)

    async def __get_model_response(self, messages, stream=True):
        _idp_session = IdpSession.get_idp_session()
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

    async def message_id(self, content: str) -> str:
        message_id = Utils.simple_uuid4()
        await RedisService.set(RedisKey.message_status(message_id), MessageStatus.NORMAL.value, 24 * 60 * 60)
        await RedisService.set(RedisKey.message_content(message_id), content, 24 * 60 * 60)
        return message_id

    async def meeting_summary(self, message_id: str) -> str:
        """
        会议总结处理
        :param message_id: 消息编号
        :return: 会议总结
        """
        content = await self.__check_and_get_content(message_id)
        messages = [
            {"role": "system", "content": self.__get_system_prompt()},
            {"role": "user", "content": self.__get_user_prompt(content)}
        ]
        start_time = time.time()
        try:
            response = await self.__get_model_response(messages=messages, stream=False)
            result = response['choices'][0]['message']['content']
        except Exception as e:
            log.exception("发生异常：%s", str(e))
            result = self.__get_exp_msg(e)
        finally:
            log.debug(f'请求耗时：{time.time() - start_time:.2f} s')
        return result

    async def meeting_summary_sse(self, message_id: str):
        """
        会议总结处理，SSE
        :param message_id: 消息编号
        :return: 会议总结推送生成器
        """
        content = await RedisService.get(RedisKey.message_content(message_id))

        yield "event:initializing\ndata:Initializing...\n\n"

        if content:
            await RedisService.set(RedisKey.message_status(message_id), MessageStatus.NORMAL.value, 24 * 60 * 60)

            messages = [
                {"role": "system", "content": self.__get_system_prompt()},
                {"role": "user", "content": self.__get_user_prompt(content)}
            ]
            start_time = time.time()
            try:
                response = await self.__get_model_response(messages=messages)
                log.debug(f'请求耗时：{time.time() - start_time:.2f} s')
                for chunk in response:
                    msg_status = await RedisService.get(RedisKey.message_status(message_id))
                    if MessageStatus.STOP.value == msg_status:
                        response.close()
                        break
                    delta = chunk.choices[0].delta
                    if "content" in delta:
                        _content = delta['content']
                        if _content:
                            if '\n' == _content:
                                _content = '\\n'
                            yield "data:{}\n\n".format(_content)
                            await asyncio.sleep(0.1)
            except Exception as e:
                log.exception("发生异常：%s", str(e))
                yield "data:{}\n\n".format(self.__get_exp_msg(e))
        else:
            yield "data:{}\n\n".format('会议内容不存在')

        # 处理完成
        yield "event:completed\ndata:Completed\n\n"
        yield "event:end\ndata:End\n\n"

    async def meeting_summary_sse_stop(self, message_id: str) -> bool:
        """
        停止会议总结处理
        :param message_id: 消息编号
        :return: 停止结果：true-成功，false-失败
        """
        coroutine = await RedisService.set(RedisKey.message_status(message_id), MessageStatus.STOP.value, 24 * 60 * 60)
        return bool(coroutine)

    def __get_exp_msg(self, e):
        """
        获取异常信息
        :param e:
        :return:
        """
        msg = '网络异常，请稍后再试'
        if isinstance(e, openai.error.APIError):
            if 'API rate limit exceeded' == e.json_body['message']:
                msg = '请求次数超限，请稍后再试'
        return msg

    async def __check_and_get_content(self, message_id) -> str:
        """
        检查并获取消息内容
        :param message_id:
        :return:
        """
        content = await RedisService.get(RedisKey.message_content(message_id))
        if not content:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "会议内容不存在")
        return content


def meeting_service() -> MeetingService:
    """会议服务单例实例"""
    return MeetingService()
