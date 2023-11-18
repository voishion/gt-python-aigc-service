#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : App运行时文件
    Author  : Lu Li (李露)
    File    : app.py
    Date    : 2023/11/16 14:48
    Site    : https://gitee.com/voishion
    Project : gt-python-aigc-service
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from tortoise.exceptions import OperationalError, DoesNotExist, IntegrityError, ValidationError

from config import settings
from core import Exception, Events, Router, Middleware
from core.Logger import Loggers

application = FastAPI(
    debug=settings.APP_DEBUG,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL,
)


# custom_openapi
def custom_openapi():
    if application.openapi_schema:
        return application.openapi_schema
    openapi_schema = get_openapi(
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        title=settings.PROJECT_NAME,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo-teal.png"
    }
    application.openapi_schema = openapi_schema
    return application.openapi_schema


application.openapi = custom_openapi


# custom_swagger_ui_html
@application.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=application.openapi_url,
        title=application.title + " - Swagger UI",
        oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


# swagger_ui_oauth2_redirect_url
@application.get(application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


# redoc
@application.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=application.openapi_url,
        title=application.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# 事件监听
application.add_event_handler("startup", Events.startup(application))
application.add_event_handler("shutdown", Events.stopping(application))

# 异常错误处理
application.add_exception_handler(HTTPException, Exception.http_error_handler)
application.add_exception_handler(RequestValidationError, Exception.http422_error_handler)
application.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)
application.add_exception_handler(DoesNotExist, Exception.mysql_does_not_exist)
application.add_exception_handler(IntegrityError, Exception.mysql_integrity_error)
application.add_exception_handler(ValidationError, Exception.mysql_validation_error)
application.add_exception_handler(OperationalError, Exception.mysql_operational_error)

# 中间件
application.add_middleware(Middleware.BaseMiddleware)

application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

application.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE,
    max_age=settings.SESSION_MAX_AGE
)


# @application.middleware("http")
# async def request_trace_id_middleware(request: Request, call_next):
#     trace_id = str(uuid.uuid4())
#     with logger.contextualize(trace_id=trace_id):
#         try:
#             logger.info("Request started")
#             return await call_next(request)
#         except Exception as exc:
#             logger.error(f"Request failed: {exc}")
#             return JSONResponse({
#                 "code": -1,
#                 "message": exc.__str__(),
#                 "data": []
#             }, status_code=500)
#         finally:
#             logger.info("Request ended")


# 路由
application.include_router(Router.router)

# 静态资源目录
application.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name="static")
application.state.views = Jinja2Templates(directory=settings.TEMPLATE_DIR)

# loguru接管uvicorn日志
Loggers.init_config()

app = application
