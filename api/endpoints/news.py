#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 新闻处理
    Author  : Lu Li (李露)
    File    : news.py
    Date    : 2023/11/20 15:08
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
from fastapi import APIRouter

from core.Response import success
from schemas import news
from service.news_service import news_service

router = APIRouter(prefix='')


@router.post(
    path='/search',
    summary="新闻搜索",
    description="通过人工智能实现搜索并总结搜索结果",
    response_model=news.NewsSearchResp,
)
async def summary(post: news.NewsSearchReq):
    result = await news_service().search(post.prompt)
    return success(msg="新闻搜索完成", data=result)
