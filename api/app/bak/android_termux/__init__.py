# import os
# import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from utils import responses as resp
# from utils.responses import response_with


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="../dist/static", html=True), name="static")
    templates = Jinja2Templates(directory="../dist")
    # 注册插件
    register_routers(app)
    return app


def register_routers(app):  # 只有在此处注册的应用才可以自动生成数据表
    from app.azquotes import routes as azquotes_routes
    app.include_router(azquotes_routes.router, prefix='/api/azquotes', tags=['azquotes'])

    from app.system_info import routes as system_info_routes
    app.include_router(system_info_routes.router, prefix='/api/system_info', tags=['system_info'])

    from app.jiucaigongshe import routes as jiucaigongshe_routes
    app.include_router(jiucaigongshe_routes.router, prefix='/api/jiucaigongshe', tags=['jiucaigongshe'])

    from app.liepin import routes as liepin_routes
    app.include_router(liepin_routes.router, prefix='/api/liepin', tags=['liepin'])

    from app.netease_music import routes as netease_music_routes
    app.include_router(netease_music_routes.router, prefix='/api/netease_music', tags=['netease_music'])

    # from app.pcap_analysis import routes as pcap_analysis_routes
    # app.include_router(pcap_analysis_routes.router, prefix='/api/pcap_analysis', tags=['pcap_analysis'])

    from app.databases import routes as databases_routes
    app.include_router(databases_routes.router, prefix='/api/databases', tags=['databases'])

    from app.qiyewechat import routes as qiyewechat_routes
    app.include_router(qiyewechat_routes.router, prefix='/api/qiyewechat', tags=['qiyewechat'])
