# from app.jiucaigongshe.schema import blockSearchScheme
import datetime
import re
import time
from urllib.parse import urljoin

import execjs
# import requests
import aiohttp
import asyncio
from fastapi import APIRouter
from lxml import etree
from utils import check_proxy
from utils import responses as resp
from utils.responses import response_with

today = time.strftime('%Y-%m-%d')  # 当天日期
yesterday = str(datetime.date.today() - datetime.timedelta(days=1))  # 昨日日期
router = APIRouter()


class JYGS:
    def __init__(self, ) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
            }
        self.cookies = {
            'SESSION': 'Y2Y1MTdjN2YtNmY3Ni00MzJlLWJhN2ItMTIwOWQ1OTljMTgx',
            'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1730815202',
            'UM_distinctid': '192fca0141e34d-06f47c9e9ba581-1f525636-4da900-192fca0141fe8d',
            'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1730815435',
        }

    async def get_jiuyangongshe_data_by_api(self, time_str: str) -> dict:
        print(f'正在获取 <{time_str}> 的数据')
        json_data = {
            'date': time_str,
            'pc': 1,
        }
        current_time = str(int(time.time() * 1000))
        self.headers['platform'] = '3'
        self.headers['content-type'] = 'application/json;charset=UTF-8'
        self.headers['timestamp'] = current_time
        self.headers['token'] = execjs.compile(open('api_js/jiuyangongshe_api.js', 'r', encoding='utf-8').read()).call('get_token_by_time', current_time)
        async with aiohttp.ClientSession() as session:
            if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                async with session.post('https://app.jiuyangongshe.com/jystock-app/api/v1/action/field',
                cookies=self.cookies,
                headers=self.headers,
                json=json_data,
                proxy=check_proxy()['http']) as response:
                    response_json = await response.json()
            else:
                async with session.post('https://app.jiuyangongshe.com/jystock-app/api/v1/action/field',
                cookies=self.cookies,
                headers=self.headers,
                json=json_data) as response:
                    response_json = await response.json()
        if response_json.get('errCode') != '1':  # 2024.11.05发现登录失效了,已经开始加了用户cookie检测
            if not len(response_json.get('data')[1:]):
                print(f'    当天异动分析数据为空!查询上一个交易日数据分析结果.')
                return {'data': []}
            else:  # {"msg":"登录失效","data":{},"errCode":"1","serverTime":1730814117}
                return response_json
        else:  # {"msg":"","data":{"all":234,"date":"2024-11-05","recommend":18},"errCode":"0","serverTime":1730815441}
            print(response_json.get('msg'))
            return response_json.get('msg')

    async def get_jiuyangonshe_data_today(self, time_str):  # 从2024.04.16开始似乎改成API返回数据形式了,后面估计要做反爬.
        print(f'正在获取 <{time_str}> 的数据')
        async with aiohttp.ClientSession() as session:
            if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                async with session.get(f'https://www.jiuyangongshe.com/action/{time_str}', headers=self.headers, proxy=check_proxy()['http']) as response:
                    response_text = await response.text()
            else:
                async with session.get(f'https://www.jiuyangongshe.com/action/{time_str}', headers=self.headers) as response:
                    response_text = await response.text()
        # response = requests.get(f'https://www.jiuyangongshe.com/action/{time_str}', headers=self.headers, proxies=check_proxy())
        # response.encoding = response.apparent_encoding
        try:
            script = re.findall(
            "<script>window.__NUXT__=([^<]+);</script>", response_text)[0].replace('\\u002F', "/")
            data = execjs.eval(script)  # python调用execjs执行方法
            # print(data)
            if not data.get('data')[0].get('allCount'):
                print(f'    当天异动分析数据为空!查询上一个交易日数据分析结果.')
            return data
        except IndexError:
            return

    async def get_data_new(self, time_str: str) -> list:
        data = await self.get_jiuyangongshe_data_by_api(time_str)
        i = 1
        today_str = datetime.date.today()
        past_data = False
        while not (data != '登录失效' and len(data.get('data')[1:])):
            past_n_days_str = str(today_str - datetime.timedelta(days=i))
            try:
                data = self.get_jiuyangonshe_data_today(past_n_days_str)
            except Exception as e:
                actionFieldList = []
                return actionFieldList
            i += 1
            past_data = True
        if past_data:
            actionFieldList = [i for i in data.get('data')[0].get('actionFieldList') if i.get('action_field_id')]
        else:
            actionFieldList = [i for i in data.get('data')[1:]]
        return actionFieldList


@router.get('/')
async def get_stock_info():  # 目前只能获取当天的数据
    jygs = JYGS()
    value = await jygs.get_data_new(today)
    if not value:
        value = await jygs.get_data_new(yesterday)
    value = {'searchResults': [{'id': j['name'] + '*' + str(j['count']), 'url_title': j['list']} for j in value]}
    return response_with(resp.SUCCESS_200, value=value)
