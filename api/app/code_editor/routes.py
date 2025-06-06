from app.code_editor import code_editor_bp
from app.utils import responses as resp
from app.utils.responses import response_with
from flask import request
import os


@code_editor_bp.route('/save_code', methods=['POST'])
def save_code():
    data = request.json
    filename = data['filename']
    code = data['code']
    save_path = os.path.abspath('') + '/CodeRepo/' + filename  # +'/CodeRepo/'+filename
    try:
        with open(save_path, 'w', encoding='utf-8') as f:  # , 'CodeRepo', filename)
            f.write(code)
        value = {'code': 'success', 'saved_path': save_path}  # success -> 20000 ?
    except Exception as e:
        value = {'code': 'fail', 'saved_path': save_path}
    return response_with(resp.SUCCESS_200, value=value)
