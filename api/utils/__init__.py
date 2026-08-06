# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: __init__.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 11月 05, 2024 17:53
# ---
import ipaddress
import os
import platform
import socket
import subprocess
import sys
import urllib.request
from functools import lru_cache

import yaml

system = platform.system()


def is_connected():
    """如果连接到公网则返回True，没有连接到则返回False。"""
    try:
        # 尝试连接到一个公共的 DNS 服务器
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        return True
    except OSError:
        return False


def get_os_type():  # 获取机器的架构类型
    if sys.platform.startswith("win") or system == "Windows":
        # print("当前系统是 Windows")
        return 'Windows'
    elif ((sys.platform.startswith("linux") or system == "Linux") and
          platform.system().lower() == 'linux' and
          platform.machine() == 'aarch64'):
        # print("当前系统是 Android")
        return 'Android'
    elif sys.platform.startswith("linux") or system == "Linux":
        # print("当前系统是 Linux")
        return 'Linux'
    elif sys.platform.startswith("darwin") or system == "Darwin":
        # print("当前系统是 MacOS")
        return 'MacOS'
    else:
        # print("当前系统是其他操作系统")
        return 'Unknown'


def get_local_ip_win():
    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        ipv4_str = [i for i in result.stdout.split('WLAN')[1].split('\n') if 'IPv4' in i][0]
        return ipv4_str.split(':')[1].strip()
    except (IndexError, subprocess.CalledProcessError, OSError):
        return '127.0.0.1'


def get_local_ip_linux():
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        if 'wlan' in result.stdout:
            ipv4_str = [i for i in result.stdout.split('wlan')[1].split('\n') if 'netmask 255.255.255.0' in i][0]
            return ipv4_str.split('netmask')[0].split('inet')[1].strip()
        else:  # 考虑到不在局域网下只有移动蜂窝网络的情况
            return '127.0.0.1'
    except (IndexError, subprocess.CalledProcessError, OSError):
        return '127.0.0.1'


def get_local_ip_mac():
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        ipv4_str = [i for i in result.stdout.split('en0:')[1].split('\n\t') if 'netmask 0xffffff00' in i][0]
        return ipv4_str.split('netmask')[0].split('inet')[1].strip()
    except (IndexError, subprocess.CalledProcessError, OSError):
        return '127.0.0.1'


def get_local_ip_by_route():
    """通过 UDP 连接到外部地址探测本机出口 IP。

    不实际发包、不依赖 ifconfig、不依赖网卡名，跨平台最可靠。
    若本机无网络路由则回退到 127.0.0.1。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接不发包，仅用于让 OS 选定出口网卡并返回其 IP
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


@lru_cache(maxsize=1)
def load_server_config():
    """读取 config.yaml 中的 server 配置，失败则返回空 dict。"""
    cfg_path = os.path.join(os.path.abspath('..'), 'config.yaml')
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        return data.get('server', {}) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _is_usable_host(ip: str) -> bool:
    """判断 IP 是否可作为对外访问地址（非回环/非通配）。"""
    try:
        obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return not obj.is_loopback and not obj.is_unspecified


def get_local_ip():
    """获取本机对外的 IPv4 地址，优先级：
    1) 动态路由探测（最可靠，跨平台）
    2) config.yaml 中显式配置的可用 host
    3) 原 per-OS 网卡解析（兜底）
    4) 127.0.0.1
    """
    # 1) 动态探测
    route_ip = get_local_ip_by_route()
    if _is_usable_host(route_ip):
        return route_ip

    # 2) 配置覆盖（仅当配置写了具体可用 IP 时才采用，避免采用 0.0.0.0/127.0.0.1）
    cfg_host = load_server_config().get('host', '')
    if _is_usable_host(str(cfg_host)):
        return str(cfg_host)

    # 3) 原 per-OS 解析兜底
    os_type = get_os_type()
    if os_type == 'Windows':
        return get_local_ip_win()
    elif os_type in ['Android', 'Linux']:
        return get_local_ip_linux()
    elif os_type == 'MacOS':
        return get_local_ip_mac()

    # 4) 最终兜底
    return '127.0.0.1'


def get_preferred_host():
    """返回对外可访问的 host，供前端/浏览器跳转使用。

    优先动态 IP；若配置显式写了可用的非回环 IP 也尊重配置。
    返回 127.0.0.1 时表示当前无可用局域网地址。
    """
    return get_local_ip()


def check_proxy():
    """检查联网代理之前，先检查有没有连上公网。"""
    proxy = {}
    http_proxy = ''
    if is_connected():
        proxy_handler = urllib.request.getproxies()
        if proxy_handler:
            # print("Detected proxy settings:")
            for key, value in proxy_handler.items():
                if key == 'http':
                    # print(f"{key}: {value}")
                    http_proxy = value
                    break
            proxy['http'] = http_proxy
            proxy['https'] = http_proxy
            return proxy
        else:
            # print("No proxy detected.")
            return  # {'http': 'http://127.0.0.1:443', 'https': 'http://127.0.0.1:443'}
    else:  # 离线状态
        return


# if __name__ == '__main__':
#     server_ip = get_local_ip()
#     print(get_local_network_ip_mac(server_ip))
