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
import yaml

from common.enums import NacosConfigType
from common.singleton import singleton
from config import settings
from core.Logger import log


@singleton
class NacosConfig(object):
    """
    Nacos配置信息
    """

    __nacos_config = {}

    def __init__(self):
        super().__init__()

    def set(self, key, value):
        """
        设置值
        :param key: 键
        :param value: 值
        :return: 值
        """
        self.__nacos_config[key] = value
        return value

    def get(self, key, default_value=None):
        """
        获取值
        :param key: 键
        :param default_value: 默认值
        :return: 值
        """
        if key in self.__nacos_config:
            return self.__nacos_config.get(key)
        else:
            if default_value:
                return default_value
            else:
                return None

    def clear(self):
        """
        清空配置
        :return:
        """
        self.__nacos_config.clear()

    @property
    def LFASR_APP_ID(self):
        """科大讯飞_语音转写_APPID"""
        return self.get('LFASR_APP_ID')

    @property
    def LFASR_ACCOUNT_ID(self):
        """科大讯飞_语音转写_ACCOUNT_ID"""
        return self.get('LFASR_ACCOUNT_ID')

    @property
    def LFASR_SSO_SESSION_ID(self):
        """科大讯飞_语音转写_SSO_SESSION_ID"""
        return self.get('LFASR_SSO_SESSION_ID')


nacos_config: NacosConfig = NacosConfig()
"""Nacos配置信息单例实例"""

client = nacos.NacosClient(settings.NACOS_SERVER_ADDRESSES,
                           namespace=settings.NACOS_NAMESPACE,
                           username=settings.NACOS_USERNAME,
                           password=settings.NACOS_PASSWORD)
"""NacosClient连接对象"""


def refresh_config(config_list):
    """
    刷新properties配置
    :param config_list:
    :return:
    """
    nacos_config.clear()
    for config_item in config_list:
        if config_item.find('=') > 0:
            strs = config_item.replace('\n', '').split('=')
            nacos_config.set(strs[0], strs[1])


def convert_to_list(data_dist):
    """
    转列表
    :param data_dist:
    :return:
    """

    def flatten_dict(data, parent_key='', sep='.'):
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(flatten_dict(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)

    flattened_data = flatten_dict(data_dist)
    return ['{}={}'.format(k, v) for k, v in flattened_data.items()]


async def init(data_id, group):
    """
    初始化
    :param data_id:
    :param group:
    :return:
    """
    config_type = settings.NACOS_CONFIG_TYPE
    if NacosConfigType.PROPERTIES.value == config_type:
        config_list = client.get_config(data_id, group).split("\n")
    else:
        config_data = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
        config_list = convert_to_list(config_data)
    refresh_config(config_list)
    log.info("Nacos配置初始化...")


def nacos_data_change_callback(config):
    """
    Nacos数据变动回调函数
    :param config:
    :return:
    """
    config_type = settings.NACOS_CONFIG_TYPE
    if NacosConfigType.PROPERTIES.value == config_type:
        config_list = config['content'].split("\n")
    else:
        config_data = yaml.load(config['content'], Loader=yaml.FullLoader)
        config_list = convert_to_list(config_data)
    refresh_config(config_list)
    log.info("Nacos配置更新...")


async def nacos_event_listener():
    format_list = [x.value for x in NacosConfigType]
    config_type = settings.NACOS_CONFIG_TYPE
    if config_type not in format_list:
        raise TypeError(
            '系统仅支持{}格式的nacos配置解析，不支持{}格式，请切换格式与配置'.format(','.join(format_list), config_type))

    """
    Nacos事件监听
    :return:
    """
    group = settings.NACOS_GROUP
    data_id = settings.NACOS_DATA_ID

    # 初始化
    await init(data_id, group)

    # Nacos配置监听，用于数据变动监听
    client.add_config_watcher(data_id=data_id, group=group, cb=nacos_data_change_callback)
