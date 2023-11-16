#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 说明
    Author  : Lu Li (李露)
    File    : main_remote.py.py
    Date    : 2023/11/16 16:12
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
import time
import traceback
from typing import List

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from loguru import logger

from ChatGLM3Remote import ChatGLM3Remote
from config import settings
from tool.News import News
from tool.Weather import Weather


def run_tool(tools, llm, prompt_chain: List[str]) -> dict:
    loaded_tolls = []
    for tool in tools:
        if isinstance(tool, str):
            loaded_tolls.append(load_tools([tool], llm=llm)[0])
        else:
            loaded_tolls.append(tool)
    agent = initialize_agent(
        loaded_tolls, llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    result = {}
    for prompt in prompt_chain:
        value = agent.run(prompt)
        result[prompt] = value

    return result


if __name__ == "__main__":
    llm = ChatGLM3Remote()
    llm.load_model(server_url=settings.CHATGLM3_SERVER_URL)

    # arxiv: 单个工具调用示例 1
    # run_tool(["arxiv"], llm, [
    #     "帮我查询GLM-130B相关工作"
    # ])

    # weather: 单个工具调用示例 2
    # run_tool([Weather()], llm, [
    #     "今天北京天气怎么样？",
    #     "What's the weather like in Shanghai today",
    # ])

    # calculator: 单个工具调用示例 3
    # run_tool([Calculator()], llm, [
    #     "12345679乘以54等于多少？",
    #     "3.14的3.14次方等于多少？",
    #     "根号2加上根号三等于多少？",
    # ]),

    # arxiv + weather + calculator: 多个工具结合调用
    # run_tool([Calculator(), "arxiv", Weather()], llm, [
    #     "帮我检索GLM-130B相关论文",
    #     "今天北京天气怎么样？",
    #     "根号3减去根号二再加上4等于多少？",
    # ])

    # news: 新闻搜索工具调用示例
    # 成功提示词：
    # 数科公司举办过哪些读书分享会？请注意新闻摘要日期，忽略新闻发布日期。
    # run_tool([News()], llm, [
    #     "数科公司举办过哪些读书分享会？请注意新闻摘要日期，忽略新闻发布日期，以列表的方式回答。",
    #     "数科公司举办过哪些读书分享会？请注意新闻摘要日期，忽略新闻发布日期。",
    #     "数科公司举办过哪些读书分享会？请注意新闻摘要日期，忽略新闻发布日期，忽略所属部门，以列表的方式回答。",
    #     "数科举办过哪些读书分享会？请注意新闻摘要日期，忽略新闻发布日期，以列表的方式回答。",
    #     "数科举办过哪些读书分享会？请注意新闻摘要日期，忽略新闻发布日期。",
    #     "查询数科公司读书分享会相关信息，分析举办过哪些读书分享会，请注意新闻摘要日期，忽略新闻发布日期。",
    #     "帮我搜索与数科公司相关的新闻？",
    #     "近期有哪些专题学习？",
    #     "帮我查询集团领导赴金砖国家新开发银行拜访交流相关信息？"
    # ])

    while True:
        query = input("请输入:")
        if "end" == query:
            break

        begin_time = time.time()
        try:
            # result = run_tool([Calculator(), "arxiv", Weather(), News()], llm, [query])
            # result = run_tool(["arxiv", Weather(), News()], llm, [query])
            # result = run_tool([Weather(), News()], llm, [query])
            result = run_tool([News()], llm, [query])
            # logger.info(f"result type:{type(result)}")
            # logger.info(f"result value:{json.dumps(result, ensure_ascii=False)}")
            time.sleep(0.4)
            logger.info(f'Final Result>>>>>>>>')
            time.sleep(0.1)
            print(result.get(query))
        except:
            logger.error(traceback.format_exc())
        finally:
            logger.debug(f'执行耗时：{time.time() - begin_time:.2f} s\n')
