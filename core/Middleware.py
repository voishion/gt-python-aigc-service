#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 中间件
    Author  : Lu Li (李露)
    File    : Middleware.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

import time

from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send, Message

from common import const
from common.const import IDP_SESSION, DEFAULT_IDP_SESSION, REQUEST_ID_KEY, TASK_ID_KEY, AUTHORIZATION
from core import Utils
from core.Logger import log
from core.Tl import IdpSession, TraceID
from core.Utils import random_str


class BaseMiddleware:
    """
    Middleware
    """

    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        req = Request(scope, receive, send)
        if not req.session.get("session"):
            req.session.setdefault("session", random_str())

        async def send_wrapper(message: Message) -> None:
            process_time = time.time() - start_time
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(process_time))
            await send(message)

        await self.app(scope, receive, send_wrapper)


class RequestMiddleware(BaseHTTPMiddleware):
    """
    请求中间件
    """

    async def dispatch(self, request: Request, call_next):
        try:
            # log.debug("Request started")
            idp_session = (request.cookies[IDP_SESSION] if IDP_SESSION in request.cookies else '')

            if not idp_session:
                idp_session = (request.headers[AUTHORIZATION] if AUTHORIZATION in request.headers else DEFAULT_IDP_SESSION)
                if idp_session.startswith('Bearer '):
                    idp_session = idp_session.replace('Bearer ', '')

            IdpSession.set_idp_session(idp_session)

            req_id = request.headers.get(REQUEST_ID_KEY, const.EMPTY_STR)
            if not req_id:
                req_id = Utils.uuid4()
            TraceID.set_req_id(req_id)

            response = await call_next(request)

            response.headers[REQUEST_ID_KEY] = TraceID.get_req_id()
            response.headers[TASK_ID_KEY] = TraceID.get_task_id()
            return response
        except Exception as exc:
            log.error(f"Request failed: {exc}")
            return JSONResponse(
                {
                    "code": -1,
                    "message": exc.__str__(),
                    "data": [],
                },
                status_code=500,
            )
        finally:
            # log.debug("Request ended")
            pass
