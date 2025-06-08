# from app.code_editor import code_editor_bp
# from app.utils import responses as resp
# from app.utils.responses import response_with
# from flask import request
import os

import asyncio
from fastapi import APIRouter
from pydantic import BaseModel
from utils import responses as resp
from utils.responses import response_with
import platform

if platform.system() != 'Windows':
    import uvloop
    # 使用 uvloop 作为事件循环
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
router = APIRouter()


# 定义请求体模型 (使用Pydantic进行自动验证)
class CodeSaveRequest(BaseModel):
    filename: str
    code: str


# @code_editor_bp.route('/save_code', methods=['POST'])
# def save_code():
#     data = request.json
#     filename = data['filename']
#     code = data['code']
#     save_path = os.path.abspath('') + '/CodeRepo/' + filename  # +'/CodeRepo/'+filename
#     try:
#         with open(save_path, 'w', encoding='utf-8') as f:  # , 'CodeRepo', filename)
#             f.write(code)
#         value = {'code': 'success', 'saved_path': save_path}  # success -> 20000 ?
#     except Exception as e:
#         value = {'code': 'fail', 'saved_path': save_path}
#     return response_with(resp.SUCCESS_200, value=value)


@router.post('/save_code')  # 异步版本
async def save_code(request: CodeSaveRequest):  # 目前只能获取当天的数据
    # data = request.json
    # filename = data['filename']
    print('ok saved')
    code = request.code
    # 创建存储目录 (确保目录存在)
    save_dir = os.path.abspath('') + '/CodeRepo/'
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, request.filename)
    try:
        with open(save_path, 'w', encoding='utf-8') as f:  # , 'CodeRepo', filename)
            f.write(code)
        value = {'code': 'success', 'saved_path': save_path}  # success -> 20000 ?
    except Exception as e:
        value = {'code': 'fail', 'saved_path': save_path}
    return response_with(resp.SUCCESS_200, value=value)
