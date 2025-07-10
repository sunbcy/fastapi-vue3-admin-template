from fastapi.responses import JSONResponse

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Invalid fields found"
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters."
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

FORBIDDEN_403 = {
    "http_code": 403,
    "code": "notAuthorized",
    "message": "You are not authorised to execute this."
}
UNAUTHORIZED_401 = {
    "http_code": 401,
    "code": "notAuthorized",
    "message": "Invalid authentication."
}

NOT_FOUND_HANDLER_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "route not found"
}

SUCCESS_200 = {
    'http_code': 200,
    'code': 20000  # 'success'
}

SUCCESS_201 = {
    'http_code': 201,
    'code': 'success'
}

SUCCESS_204 = {
    'http_code': 204,
    'code': 'success'
}


def response_with(response, value=None, message=None, error=None, headers={}, pagination=None):
    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'FastAPI REST API'})
    return JSONResponse(result, response['http_code'], headers)


# def response_with(
#         response: dict,
#         value: dict = None,
#         message: str = None,
#         error: str = None,
#         headers: dict = None,
#         pagination: dict = None
# ) -> JSONResponse:
#     # 安全处理默认值
#     headers = headers or {}
#     result = {}
#
#     # 按优先级合并字段
#     if value:
#         result.update(value)
#
#     # 显式处理核心字段（避免覆盖）
#     result['code'] = response.get('code', 'unknown')
#
#     # 消息处理（参数优先于response配置）
#     if message:
#         result['message'] = message
#     elif 'message' in response:
#         result['message'] = response['message']
#
#     # 错误处理（统一使用单数）
#     if error:
#         result['error'] = error
#
#     # 分页信息
#     if pagination:
#         result['pagination'] = pagination
#
#     # 状态码处理
#     http_code = response.get('http_code', 200)
#
#     # 移除硬编码CORS（应在中间件处理）
#     # headers.update({'server': 'FastAPI REST API'})
#
#     return JSONResponse(result, status_code=http_code, headers=headers)
