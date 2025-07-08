import os
import subprocess
import warnings
import webbrowser

import yaml
# from app.azquotes.routes import client
from fastapi.responses import FileResponse

from app import create_app
from utils import get_os_type

warnings.simplefilter("ignore")
app = create_app()


@app.get("/")
async def index():
    return FileResponse("../dist/index.html")

# # 在应用关闭时关闭会话
# @app.on_event("shutdown")
# async def on_shutdown():
#     await client.close_session()

PROJ_PATH = os.path.abspath('..')
with open(os.path.join(PROJ_PATH, 'config.yaml'), 'r') as file:
    net_addr = yaml.safe_load(file)

os_type = get_os_type()


# 启动应用
if __name__ == "__main__":
    if os_type == 'Windows' or os_type == 'MacOS':
        if net_addr.get('server').get('run_mode') == 1:  # ngrok外网发布地址
            webbrowser.open(f"{net_addr.get('server').get('ngrok_pub_addr')}")
            # 研究自动弹起无跳转页面的方式没意义,因为每个被转发的人都会显示.
            # webbrowser.open(f"http://{net_addr.get('server').get('host')}:{net_addr.get('server').get('port')}/pub")
        else:
            webbrowser.open(f"http://{net_addr.get('server').get('host')}:{net_addr.get('server').get('port')}")
    elif os_type == 'Android':
        if net_addr.get('server').get('run_mode') == 1:  # ngrok外网发布地址
            subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW',
                            '-d', f"{net_addr.get('server').get('ngrok_pub_addr')}"])
        else:
            subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW',
                            '-d', f"http://{net_addr.get('server').get('host')}:{net_addr.get('server').get('port')}"])
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5055)  # test  test by lly

