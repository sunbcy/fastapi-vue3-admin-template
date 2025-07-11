import asyncio
import os
import platform
# import aiofiles

from fastapi import APIRouter
from pydantic import BaseModel
from utils import responses as resp
from utils.responses import response_with

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
def save_code(request: CodeSaveRequest):  # 目前只能获取当天的数据
    print('ok saved')
    code = request.code
    # 创建存储目录 (确保目录存在)
    save_dir = os.path.abspath('') + '/CodeRepo/'
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, request.filename)
    try:
        with open(save_path, 'w', encoding='utf-8') as f:  # , 'CodeRepo', filename)
            f.write(code)
        # 使用异步文件写入
        # async with aiofiles.open(save_path, 'w', encoding='utf-8') as f:
        #     await f.write(code)
        # value = {'code': 20000, 'saved_path': save_path}  # success -> 20000 ?
        value = {'saved_path': save_path}
        print('成功写入code')
        print(response_with(resp.SUCCESS_200, value=value).body.decode("utf-8"))
    except Exception as e:
        value = {'code': 'fail', 'saved_path': save_path}
        print('写入失败')
    return response_with(resp.SUCCESS_200, value=value)
