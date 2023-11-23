#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Nacos配置
    Author  : Lu Li (李露)
    File    : Nacos.py
    Date    : 2023/11/22 17:02
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

import nacos

from config import settings
from core.Logger import log

client = nacos.NacosClient(settings.NACOS_SERVER_ADDRESSES,
                           namespace=settings.NACOS_NAMESPACE,
                           username=settings.NACOS_USERNAME,
                           password=settings.NACOS_PASSWORD)
"""NacosClient连接对象"""

nacosConfig = {}
"""Nacos配置信息"""


def refresh_properties_config(config_list):
    """
    刷新properties配置
    :param config_list:
    :return:
    """
    global nacosConfig
    for config_item in config_list:
        if config_item.find('=') > 0:
            strs = config_item.replace('\n', '').split('=')
            nacosConfig[strs[0]] = strs[1]


async def init(data_id, group):
    """
    初始化
    :param data_id:
    :param group:
    :return:
    """
    # 换行符进行分割，存入列表中
    config_list = client.get_config(data_id, group).split("\n")
    refresh_properties_config(config_list)
    log.info("Nacos配置初始化...")


def nacos_data_change_callback(config):
    """
    Nacos数据变动回调函数
    :param config:
    :return:
    """
    config_list = config['content'].split("\n")
    refresh_properties_config(config_list)
    log.info("Nacos配置更新...")


async def nacos_event_listener():
    """
    Nacos事件监听
    :return:
    """
    group = "DEFAULT_GROUP"
    data_id = "{}-{}.properties".format(settings.PROJECT_NAME, settings.RUN_ENV)

    # 初始化
    await init(data_id, group)

    # Nacos配置监听，用于数据变动监听
    client.add_config_watcher(data_id=data_id, group=group, cb=nacos_data_change_callback)
