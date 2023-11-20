#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 搜索新闻接口
    Author  : Lu Li (李露)
    File    : search_emp_api.py
    Date    : 2023/11/1 14:13
    Site    : https://gitee.com/voishion
    Project : ChatGLM3
"""
import json
import time
import traceback

import requests

from core.IdpSession import IdpSession


def search(keyword: str) -> dict:
    """
    调用搜索新闻接口
    :param keyword: 搜索关键字
    :return: 搜索结果列表
    """
    url = "https://i.gt.cn/http/pcPortal/API_CODE_SEARCH_16012099784374136"
    data = {
        "search": keyword,
        "page": "1",
        "size": "20",
        "orderType": 0,
        "platform": "PC"
    }
    resp = __api_call(1, url, data)
    if '00000' != resp['respCode']:
        raise Exception("An interface gateway exception occurred while calling search news")
    if 0 != resp['result']['code']:
        msg = json.loads(resp['result']['msg'])['message']
        raise Exception(f"Search news failed, reason:{msg}")

    result: dict = resp['result']['data']
    return result


def __recognize_opt_desc(opt_type: int):
    ens: str = ''
    cns: str = ''
    if 1 == opt_type:
        ens = 'search'
        cns = '搜索'
    return ens, cns


def __api_call(opt_type: int, url, data):
    """
    接口调用
    :param opt_type: 操作类型 1-搜索
    :param url: 接口URL
    :param data: 上送数据
    :return: 调用结果
    """
    ens, cns = __recognize_opt_desc(opt_type)
    data = json.dumps(data)
    resp = None
    begin_time = time.time()  # type: float
    try:
        headers = {
            "Content-Type": "application/json",
            "Cookie": "_idp_session={}".format(IdpSession.get_idp_session()),
        }
        resp = requests.post(url, data=data, headers=headers)
        resp.raise_for_status()
        resp = resp.json()
    except:
        format_exc = traceback.format_exc()
        raise Exception(f"Failed to call {ens} interface, {format_exc}")
    finally:
        # log.debug(f'调用{cns}新闻接口\n'
        #              f'请求信息:\nurl={url}\nheaders={json.dumps(headers)}\ndata={data}\n'
        #              f'响应信息:\n{json.dumps(resp)}\n'
        #              f'请求耗时:{(time.time() - begin_time):.2f} s')
        pass
    return resp
