# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: __init__.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 11月 05, 2024 17:53
# ---
import platform
import socket
import subprocess
import sys
import urllib.request

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
    elif (sys.platform.startswith("linux") or system == "Linux") and platform.system().lower() == 'linux' and platform.machine() == 'aarch64':
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
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    ipv4_str = [i for i in result.stdout.split('WLAN')[1].split('\n') if 'IPv4' in i][0]
    return ipv4_str.split(':')[1].strip()


def get_local_ip_linux():
    result = subprocess.run(["ifconfig"], capture_output=True, text=True)
    if 'wlan' in result.stdout:
        ipv4_str = [i for i in result.stdout.split('wlan')[1].split('\n') if 'netmask 255.255.255.0' in i][0]
        return ipv4_str.split('netmask')[0].split('inet')[1].strip()
    else:  # 考虑到不在局域网下只有移动蜂窝网络的情况
        return '127.0.0.1'


def get_local_ip_mac():
    result = subprocess.run(["ifconfig"], capture_output=True, text=True)
    ipv4_str = [i for i in result.stdout.split('en0:')[1].split('\n\t') if 'netmask 0xffffff00' in i][0]
    return ipv4_str.split('netmask')[0].split('inet')[1].strip()


def get_local_ip():
    os_type = get_os_type()
    if os_type == 'Windows':  # os win
        return get_local_ip_win()
    elif os_type in ['Android', 'Linux']:  # os linux
        return get_local_ip_linux()
    elif os_type == 'MacOS':
        return get_local_ip_mac()
    else:
        return '127.0.0.1'


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
