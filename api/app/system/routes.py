# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: routes.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 11月 02, 2024 21:56
# ---
from traceback import print_exc

import aiohttp
import asyncio
import uvloop
from fastapi import APIRouter
from pydantic import BaseModel
from utils import responses as resp
from utils.responses import response_with


# 使用 uvloop 作为事件循环
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
router = APIRouter()


class LoginForm(BaseModel):
    username: str
    password: str


@router.post('/login')  # 异步版本
async def system_login(login_form: LoginForm):  # 目前只能获取当天的数据
    print(login_form)

    value = {'searchResults': 'ok'}
    return response_with(resp.SUCCESS_200, value=value)
