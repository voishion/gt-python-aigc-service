#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 远程调用ChatGLM3
    Author  : Lu Li (李露)
    File    : ChatGLM3Remote.py
    Date    : 2023/11/16 16:13
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""
import json
from typing import List, Optional

import openai
from langchain.llms.base import LLM
from core.Logger import log

from chatglm3.langchain.utils import tool_config_from_file


class ChatGLM3Remote(LLM):
    max_token: int = 8192
    do_sample: bool = False
    temperature: float = 0.75
    top_p = 0.8
    tokenizer: object = None
    model: object = None
    history: List = []
    tool_names: List = []
    has_search: bool = False
    server_url: str = None

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "ChatGLM3"

    def load_model(self, server_url=None):
        self.server_url = server_url

    def _tool_history(self, prompt: str):
        ans = []
        tool_prompts = prompt.split(
            "You have access to the following tools:\n\n")[1].split("\n\nUse a json blob")[0].split("\n")

        tool_names = [tool.split(":")[0] for tool in tool_prompts]
        self.tool_names = tool_names
        tools_json = []
        for i, tool in enumerate(tool_names):
            tool_config = tool_config_from_file(tool)
            if tool_config:
                tools_json.append(tool_config)
            else:
                ValueError(
                    f"Tool {tool} config not found! It's description is {tool_prompts[i]}"
                )

        ans.append({
            "role": "system",
            "content": "Answer the following questions as best as you can. You have access to the following tools:",
            "tools": tools_json
        })
        query = f"""{prompt.split("Human: ")[-1].strip()}"""
        return ans, query

    def _extract_observation(self, prompt: str):
        return_json = prompt.split("Observation: ")[-1].split("\nThought:")[0]
        self.history.append({
            "role": "observation",
            "content": return_json
        })
        return

    def _extract_tool(self):
        if len(self.history[-1]["metadata"]) > 0:
            metadata = self.history[-1]["metadata"]
            content = self.history[-1]["content"]
            if "tool_call" in content:
                for tool in self.tool_names:
                    if tool in metadata:
                        input_para = content.split("='")[-1].split("'")[0]
                        action_json = {
                            "action": tool,
                            "action_input": input_para
                        }
                        self.has_search = True
                        return f"""
Action: 
```
{json.dumps(action_json, ensure_ascii=False)}
```"""
        final_answer_json = {
            "action": "Final Answer",
            "action_input": self.history[-1]["content"]
        }
        self.has_search = False
        return f"""
Action: 
```
{json.dumps(final_answer_json, ensure_ascii=False)}
```"""

    def _call(self, prompt: str, history: List = [], stop: Optional[List[str]] = ["<|user|>"]):
        # print("======")
        # print(prompt)
        # print("======")
        if not self.has_search:
            self.history, query = self._tool_history(prompt)
        else:
            self._extract_observation(prompt)
            query = ""
        # print("======")
        # print(self.history)
        # print("======")

        self.history = self._call_remote(self.history, query)

        response = self._extract_tool()
        history.append((prompt, response))
        return response

    def _call_remote(self, history: List, query: str):
        history.append({
            "role": "user",
            "content": query
        })

        log.info(f">>>query:{type(query)}, json:{json.dumps(query, ensure_ascii=False)}")
        log.info(f">>>self.history:{type(self.history)}, json:\n{json.dumps(self.history, ensure_ascii=False)}")
        # log.info(f">>>self.do_sample:{self.do_sample}")
        # log.info(f">>>self.max_token:{self.max_token}")
        # log.info(f">>>self.temperature:{self.temperature}")

        openai.api_base = self.server_url
        openai.api_key = "any"
        chat_completion = openai.ChatCompletion.create(
            model="chatglm3",
            messages=history,
            do_sample=self.do_sample,
            max_length=self.max_token,
            temperature=self.temperature,
        )
        result = chat_completion['choices'][0]['message']
        role = result['role']
        answer = result['content'].split('\n')
        metadata = answer.pop(0)
        content = '\n'.join(answer)

        history.append({
            "role": role,
            "metadata": metadata,
            "content": content
        })

        log.info(f"<<<self.history:{type(self.history)}, json:\n{json.dumps(self.history, ensure_ascii=False)}")
        return history