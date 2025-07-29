# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: routes.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 7月 15, 2025 01:50
# ---
from traceback import print_exc

import aiohttp
import asyncio
import uvloop
from fastapi import APIRouter
from lxml import etree
from utils import check_proxy
from utils import responses as resp
from utils.responses import response_with

# 使用 uvloop 作为事件循环
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
router = APIRouter()


def deliver_quotes_to_qiyeweixin(quotes):
    if not quotes:
        return 'Where there is a will, there is a way!'
    for i in quotes:
        print(" {quote}".format(quote=quotes.get(i)))
        quote_str = """【Quote of today】\n{quote}\n\n--{author}""".format(quote=quotes.get(i), author=i)
        # Bot_1 = QiYeWeChatBot()
        # quote_str = {
        #     'text': quote_str
        # }
        # Bot_1.send_text(quote_str)
        break
    return quote_str


class AsyncQuotesBot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100, ssl=False))
        return cls._instance

    def __init__(self, proxy=check_proxy()):
        self.quote_main_url = "https://azquotes.com"
        self.quote_main_url_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
        }
        self.proxy = proxy['http'] if proxy else None
        self.connector = aiohttp.TCPConnector(limit=100, ssl=False)  # 设置连接池大小

    async def fetch(self):
        kwargs = {}
        if self.proxy:
            kwargs['proxy'] = self.proxy

        # async with aiohttp.ClientSession(connector=self.connector) as session:
        if self.proxy:
            async with self.session.get(self.quote_main_url,
                                        headers=self.quote_main_url_headers,
                                        timeout=aiohttp.ClientTimeout(total=30),
                                        **kwargs) as response:
                return await response.text()
        else:
            async with self.session.get(self.quote_main_url,
                                        headers=self.quote_main_url_headers,
                                        timeout=aiohttp.ClientTimeout(total=30)
                                        ) as response:
                return await response.text()

    async def get_today_quote(self):
        try:
            r = await self.fetch()
            html = etree.HTML(r)
            quote_today = html.xpath('//div[@class="content-slide content-slide_top"]/p/a[@class="title"]/text()')
            quote_author_today = html.xpath(
                '//div[@class="content-slide content-slide_top"]/div[@class="q_user"]/a/text()')
            print("今日Quotes获取成功!")
            quotes = dict(zip(quote_author_today, quote_today))
            return quotes
        except Exception as e:
            print_exc()
            print("今日Quotes获取失败!")
            return {}


# @azquotes_bp.route('/', methods=['GET'])  # 同步版本
# def get_today_azquote():  # 目前只能获取当天的数据
#     quote_bot = QuotesCollector()
#     quotes_dict = quote_bot.get_today_quote()
#     quote_str = deliver_quotes_to_qiyeweixin(quotes_dict)  # 企业微信发送格言
#     value = {'searchResults': quote_str}
#     return response_with(resp.SUCCESS_200, value=value)

client = AsyncQuotesBot()


@router.get('/', tags=['azquotes注册接口'])  # 异步版本
async def get_today_azquote():  # 目前只能获取当天的数据
    quotes_dict = await client.get_today_quote()
    # print(quotes_dict)
    if not quotes_dict:
        return 'Where there is a will, there is a way!'
    for i in quotes_dict:
        quote_str = """【Quote of today】\n{quote}\n\n--{author}""".format(quote=quotes_dict.get(i), author=i)
        print(quote_str)
        break
    value = {'searchResults': quote_str}
    print(response_with(resp.SUCCESS_200, value=value).body.decode("utf-8"))
    return response_with(resp.SUCCESS_200, value=value)


# if __name__ == '__main__':
#     quote_bot = QuotesCollector()
#     quotes_dict = quote_bot.get_today_quote()
#     # quote_bot.deliver_quotes_to_qiyeweixin(quotes_dict)  # 企业微信发送格言
#     # quote_bot.deliver_quotes_to_mail(quotes_dict)  # 邮件发送格言
