#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/7/15 上午2:51
# @Author  : sunbcy
# @File    : open_browser.py
# @Software: PyCharm
import os
import subprocess
import webbrowser
import yaml
from utils import get_os_type
from utils import get_preferred_host


# 启动应用
PROJ_PATH = os.path.abspath('..')
with open(os.path.join(PROJ_PATH, 'config.yaml'), 'r') as file:
    net_addr = yaml.safe_load(file)
server_cfg = (net_addr or {}).get('server', {}) or {}
os_type = get_os_type()

# 访问地址优先使用动态获取的本机 IP，配置中的 host 仅在动态获取失败(回环)时回退
host = get_preferred_host()
port = server_cfg.get('port', 5055)
pub_addr = server_cfg.get('ngrok_pub_addr', '')

if os_type == 'Windows' or os_type == 'MacOS':
    if server_cfg.get('run_mode') == 1 and pub_addr:  # ngrok外网发布地址
        webbrowser.open(pub_addr)
        # 研究自动弹起无跳转页面的方式没意义,因为每个被转发的人都会显示.
        # webbrowser.open(f"http://{host}:{port}/pub")
    else:
        webbrowser.open(f"http://{host}:{port}")
elif os_type == 'Android':
    if server_cfg.get('run_mode') == 1 and pub_addr:  # ngrok外网发布地址
        subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', pub_addr])
    else:
        subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', f"http://{host}:{port}"])
