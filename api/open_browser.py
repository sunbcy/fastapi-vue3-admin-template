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


# 启动应用
PROJ_PATH = os.path.abspath('..')
with open(os.path.join(PROJ_PATH, 'config.yaml'), 'r') as file:
    net_addr = yaml.safe_load(file)
os_type = get_os_type()
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
