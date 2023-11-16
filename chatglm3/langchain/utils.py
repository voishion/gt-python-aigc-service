#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 工具
    Author  : Lu Li (李露)
    File    : utils.py.py
    Date    : 2023/11/16 16:18
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
import os
import yaml


def tool_config_from_file(tool_name, directory="tool/"):
    """search tool yaml and return json format"""
    for filename in os.listdir(directory):
        if filename.endswith('.yaml') and tool_name in filename:
            file_path = os.path.join(directory, filename)
            with open(file_path, encoding='utf-8') as f:
                return yaml.safe_load(f)
    return None
