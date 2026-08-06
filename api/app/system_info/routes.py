# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: routes.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 7月 15, 2025 01:43
# ---
import ipaddress
import os
import re
import signal
import subprocess
import time

import nmap
import psutil
import requests
# from app.qiyewechat.routes import QiYeWeChatBot
from bs4 import BeautifulSoup
from fake_headers import Headers
from fastapi import APIRouter
from utils import check_proxy
from utils import get_local_ip
from utils import get_os_type
from utils import responses as resp
from utils.responses import response_with

# from geopy.geocoders import Nominatim
REPO_PATH = os.path.abspath('..')
router = APIRouter()


def get_cpu_info():
    # 获取 CPU 物理核心数
    physical_cores = psutil.cpu_count(logical=False)
    # 获取 CPU 逻辑核心数
    logical_cores = psutil.cpu_count(logical=True)
    # 获取 CPU 频率
    cpu_freq = psutil.cpu_freq()
    try:
        # 获取每个 CPU 核心的使用率
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_info = (f'Physical cores: {physical_cores}; '
                    f'Logical cores: {logical_cores}; '
                    f'Max Frequency: {cpu_freq.max} Mhz; '
                    f'Min Frequency: {cpu_freq.min} Mhz; '
                    f'Current Frequency: {cpu_freq.current} Mhz; '
                    f'CPU Usage Per Core: {cpu_percent}; '
                    f'Total CPU Usage: {psutil.cpu_percent(interval=1)}%; ')
    except PermissionError:
        cpu_info = (f'Physical cores: {physical_cores}; '
                    f'Logical cores: {logical_cores}; '
                    f'Max Frequency: {cpu_freq.max} Mhz; '
                    f'Min Frequency: {cpu_freq.min} Mhz; '
                    f'Current Frequency: {cpu_freq.current} Mhz; ')
    return cpu_info


def get_disk_info():
    disk_info = ''
    # 获取所有磁盘分区信息
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            # 获取分区使用情况
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total Size: {partition_usage.total / (1024 ** 3):.2f} GB")
            print(f"  Used: {partition_usage.used / (1024 ** 3):.2f} GB")
            print(f"  Free: {partition_usage.free / (1024 ** 3):.2f} GB")
            print(f"  Percentage: {partition_usage.percent}%")
            disk_info += (f'=== Device: {partition.device} ===;\n  '
                          f'Mountpoint: {partition.mountpoint};   '
                          f'File system type: {partition.fstype};\n   '
                          f'Total Size: {partition_usage.total / (1024 ** 3):.2f} GB;   '
                          f'Used: {partition_usage.used / (1024 ** 3):.2f} GB;   '
                          f'Free: {partition_usage.free / (1024 ** 3):.2f} GB;   '
                          f'Percentage: {partition_usage.percent}%;\n ')
        except PermissionError:
            pass
    # 获取所有磁盘的总I/O统计信息
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {disk_io.read_bytes / (1024 ** 3):.2f} GB")
    print(f"Total write: {disk_io.write_bytes / (1024 ** 3):.2f} GB")
    disk_info += (f'Total read: {disk_io.read_bytes / (1024 ** 3):.2f} GB;\n '
                  f'Total write: {disk_io.write_bytes / (1024 ** 3):.2f} GB\n')
    return disk_info


def get_wan_ip():
    # 获取公共 IP 地址
    ip_api_url = "https://api.ipify.org?format=json"
    try:
        if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
            response = requests.get(ip_api_url, proxies=check_proxy())
        else:
            response = requests.get(ip_api_url)
        data = response.json()
        ip = data.get('ip') if isinstance(data, dict) else None
        if not ip:
            print('ip not found!--响应中无 ip 字段')
            return
        return ip
    except requests.exceptions.ProxyError:
        print('ip not found!--ProxyError')
        return
    except requests.exceptions.SSLError:
        print('ip not found!--SSLError')
        return
    except requests.exceptions.ConnectionError:
        print('ip not found!--ConnectionError')
        return
    except (ValueError, KeyError, IndexError):
        print('ip not found!--响应解析失败')
        return


def get_position(ips):
    # 使用 ipinfo 服务获取地理位置信息
    location_api_url = f"https://ipinfo.io/{ips}/json"
    try:
        if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
            location_response = requests.get(location_api_url, proxies=check_proxy())
        else:
            location_response = requests.get(location_api_url)
        location_data = location_response.json()

        # 解析位置数据
        if 'loc' in location_data:
            loc = location_data['loc'].split(',')
            latitude = loc[0]
            longitude = loc[1]
            return latitude, longitude
        else:
            return '', ''
    except requests.exceptions.ProxyError:  # 因为网络问题获取不了数据
        return '', ''
    except requests.exceptions.SSLError:  # 因为网络问题获取不了数据
        return '', ''
    except requests.exceptions.ConnectionError:  # 因为网络问题获取不了数据
        return '', ''


def get_ip_info(ip=None):
    precnt_mode = "<pre>(.*?)</pre>"
    url = 'http://cip.cc'  # 免费的IP查询地址  会失效,502
    url = f"{url}/{ip}" if ip else f'{url}'
    headers = Headers(headers=True).generate()
    if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
        html = requests.get(url, headers=headers, proxies=check_proxy())
    else:
        html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    # print(html.text)
    soup = BeautifulSoup(html.text, 'html.parser')
    pres = soup.find_all('pre')
    if not pres:
        return f"{time.strftime('%Y-%m-%d %H:%M:%S')}\nIP: 解析失败(cip.cc 无返回)"
    content = re.findall(precnt_mode, str(pres[0]), re.S | re.M)
    if not content:
        return f"{time.strftime('%Y-%m-%d %H:%M:%S')}\nIP: 解析失败(cip.cc 格式变化)"

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n{content[0]}")
    return (f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n{content[0]}")


# def get_location(lat, lon):  # 要代理外网才能访问
#     # 使用 geopy 将经纬度转换为详细地址
#     geolocator = Nominatim(user_agent="geoapiExercises", proxies=check_proxy())
#     location = geolocator.reverse(f"{lat}, {lon}")
#     return location


def get_network_range(ip, prefix_length=24):
    # 创建一个IPv4网络对象
    network = ipaddress.ip_network(f"{ip}/{prefix_length}", strict=False)
    # 获取网络地址
    network_address = network.network_address
    # 返回CIDR表示的网络范围
    return f"{network_address}/{prefix_length}"


def get_local_network_ip_mac(server_ip):
    script_path = os.path.abspath('utils/scan_network.py')
    # 需要root权限的命令
    command = ['sudo', 'nohup', 'python3', script_path, server_ip]
    # sudo 密码从环境变量读取，避免明文写死在代码里
    # 运行前请设置: export SUDO_PASSWORD='你的密码'
    password = os.environ.get('SUDO_PASSWORD')
    if not password:
        print("Error: 未设置环境变量 SUDO_PASSWORD，无法执行需要 root 权限的局域网扫描")
        return

    # 使用 sudo -S 并直接通过 stdin 传递密码，避免密码出现在进程列表中
    sudo_process = subprocess.Popen(
        ['sudo', '-S'] + command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = sudo_process.communicate(input=password.encode('utf-8'))

    if sudo_process.returncode != 0:
        print(f"Error: {error.decode('utf-8').strip()}")
        return
    else:
        cnt_str = output.decode('utf-8').strip()[1:-1]
        mode_ip_mac = "{'ip': '(.*?)', 'mac': '(.*?)'}"
        ip_mac_list = []
        for i in re.findall(mode_ip_mac, cnt_str):
            ip, mac = i
            ip_mac_list.append({'ip': ip, 'mac': mac})
        return ip_mac_list


def git_pull(repo_path):
    print(repo_path)
    # 更改当前工作目录到你的 Git 仓库路径
    try:
        # 使用 check_call 或者 check_output 可以确保命令执行成功，并且可以捕获异常
        # check_call 会直接输出到控制台
        # subprocess.check_call(['git', 'pull'], cwd=repo_path)

        # 如果你想捕获输出，可以使用 check_output
        output = subprocess.check_output(['git', 'pull'], cwd=repo_path, stderr=subprocess.STDOUT, text=True)
        # print(output)
        if '已经是最新的。' in output:
            print('ok')
            return True
    except subprocess.CalledProcessError as e:
        # 如果 git pull 失败，则会抛出这个异常
        print(f"Git pull failed with error: {e.output}")
        return False
    except Exception as e:
        # 其他异常处理
        print(f"An error occurred: {str(e)}")
        return False


def find_process_by_port(port):
    os_type = get_os_type()
    if os_type == 'Windows':
        # 使用 netstat 查找监听指定端口的进程
        try:
            result = subprocess.run(['netstat', '-anp'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                lines = result.stdout.splitlines()
                for line in lines:
                    if f":{port}" in line and "LISTEN" in line:  # 确保是监听状态
                        parts = line.split()
                        # 获取最后一列，通常是 PID/程序名
                        pid_info = parts[-1]
                        if '/' in pid_info:
                            pid = int(pid_info.split('/')[0])  # 提取 PID
                            return pid
            else:
                print(f"Error running netstat: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error while finding process by port: {e}")
            return None
    elif os_type == 'Linux' or os_type == 'MacOS':
        # 使用 lsof 查找监听指定端口的进程
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                lines = result.stdout.splitlines()
                for line in lines[1:]:  # 跳过表头行
                    parts = line.split()
                    pid = int(parts[1])  # PID 是第二列
                    return pid
            else:
                print(f"No process found listening on port {port}: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error while finding process by port: {e}")
            return None
    elif os_type == 'Android':  # 这里恐怕有问题
        # 使用 lsof 查找监听指定端口的进程
        try:
            # 找到所有包含 "python" 或 "flask" 的进程，并过滤出包含 ":<port>" 的行
            result = subprocess.run(['ps', 'aux'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                lines = result.stdout.splitlines()
                for line in lines:
                    if ("bash" in line and "./termux_start.sh" in line) or (f'--port={port}' in line):
                        parts = line.split()
                        pid = int(parts[1])  # PID 是第二列
                        return pid
            else:
                print(f"No process found listening on port {port}: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error while finding process by port: {e}")
            return None


def kill_process(pid):
    # 杀死指定的进程
    try:
        os.kill(pid, signal.SIGTERM)  # 只是优雅地终止了进程
        print(f"Killed process with PID: {pid}")
    except ProcessLookupError:
        print(f"Process with PID {pid} does not exist.")
    except PermissionError:
        print(f"Permission denied to kill process with PID {pid}.")
    except Exception as e:
        print(f"Error while killing process {pid}: {e}")


def kill_processes(pids):
    # 杀死指定的进程
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Killed process with PID: {pid}")
        except ProcessLookupError:
            print(f"Process with PID {pid} does not exist.")
        except PermissionError:
            print(f"Permission denied to kill process with PID {pid}.")
        except Exception as e:
            print(f"Error while killing process {pid}: {e}")


def restart_script():
    # 找到并杀死所有相关的进程
    # pids = find_process_id(script_path)
    # kill_processes(pids)
    current_dir = os.path.abspath('')
    print(f'restart_script - {current_dir}')
    # os.chdir(REPO_PATH)  # 到了项目根目录
    print(f'restart_script 切换后 - {os.path.abspath("")}')
    proj_pid = find_process_by_port('5055')
    print(f'当前进程ID: {proj_pid}')
    # os.chdir(current_dir)
    try:
        subprocess.Popen(['python', os.path.abspath("../new_create_process.py")],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)  # 调用新的进程启动脚本
    except Exception:
        pass
        # qw_bot = QiYeWeChatBot()
        # qw_bot.send_text(e.output)
    kill_process(proj_pid)  # 应该本函数最后在终止进程


@router.get('/')
def get_system_info():  # 获取系统的数据
    os_type = get_os_type()
    try:
        cpu_info = get_cpu_info()
    except Exception:
        cpu_info = ''
    try:
        disk_info = get_disk_info()
    except PermissionError:
        disk_info = ''
    local_ip = get_local_ip()
    wan_ip = get_wan_ip()
    if wan_ip:
        latitude, longitude = get_position(wan_ip)
        try:
            ip_info = get_ip_info(wan_ip)
        except Exception:
            ip_info = ''
            print('get_ip_info()不可用🚫,请排查!!!')
    else:
        try:
            ip_info = get_ip_info()
        except Exception:
            ip_info = ''
            print('get_ip_info()不可用🚫,请排查!!!')
        ip_lines = [i for i in ip_info.split('\n') if 'IP' in i]
        if ip_lines:
            wan_ip = ip_lines[0].split(':')[1].strip()
            latitude, longitude = get_position(wan_ip)
        else:
            latitude, longitude = '', ''
    # location = get_location(latitude, longitude)
    value = {
        'searchResults':
            {
                'os_type': os_type,
                'cpu_info': cpu_info,
                'disk_info': disk_info,
                'local_ip': local_ip,
                'wan_ip': wan_ip,
                'latitude': latitude,
                'longitude': longitude,
                'ip_info': ip_info
            }
    }  # , 'location': location
    # print(value)
    return response_with(resp.SUCCESS_200, value=value)


@router.get('/get_lan_info')
def get_lan_info():  # 获取LAN的 host 信息
    current_dir = os.path.abspath('')
    try:
        server_ip = get_local_ip()
        ip_range = get_network_range(server_ip)
        os_type = get_os_type()
        if os_type == 'MacOS':
            print(f'get_lan_info - {current_dir}')
            ret_info = get_local_network_ip_mac(server_ip)
            value = {'searchResults': [{'deviceName': '设备' + str(ret_info.index(i) + 1),
                                        'ip': i['ip'],
                                        'mac': i['mac']} for i in ret_info]}
        elif os_type == 'Android':
            nm = nmap.PortScanner()  # 上面的代码做备用
            result = nm.scan(hosts=ip_range, arguments='-sn')
            # print(result)
            ret_info = list(result['scan'].keys())
            new_ret_info = []
            for _ in ret_info:
                ret_ip = nm.scan(hosts=_, arguments='-sn')
                try:
                    hostname = ret_ip['scan'][_]['hostnames'][0]['name']
                except KeyError:
                    print(ret_ip['scan'])
                    hostname = ''
                new_ret_info.append({'deviceName': hostname, 'ip': _, 'mac': ''})
            value = {
                'searchResults': [{
                    'deviceName': '设备' + str(new_ret_info.index(i) + 1) if not i['deviceName'] else i['deviceName'],
                    'ip': i['ip'],
                    'mac': i['mac']} for i in new_ret_info]
            }
        return response_with(resp.SUCCESS_200, value=value)
    except Exception:
        value = {'searchResults': os.path.abspath('')}
        return response_with(resp.SERVER_ERROR_404, value=value)


@router.get('/update_project')
def update_project():  # 获取LAN的 host 信息
    try:
        ret_status = git_pull(REPO_PATH)
        value = {'searchResults': ret_status}
        return response_with(resp.SUCCESS_200, value=value)
    except Exception:
        value = {'searchResults': False}
        return response_with(resp.SERVER_ERROR_404, value=value)


@router.get('/compile_project')
def compile_project():  # 获取LAN的 host 信息
    # 切换当前工作目录
    current_dir = os.path.abspath('')
    os.chdir(REPO_PATH)
    print(f"Current directory: {REPO_PATH}")
    os_type = get_os_type()
    if os_type == 'Android' or os_type == 'Linux' or os_type == 'MacOS':
        subprocess.run(["npm", "run", "build:prod"], capture_output=False, text=True)
    elif os_type == 'Windows':
        subprocess.run(["npm", "run", "build:prod"], capture_output=False, text=True, shell=True)
    else:
        print('系统未知，请手动编译项目!')
    os.chdir(current_dir)
    value = {'searchResults': True}
    return response_with(resp.SUCCESS_200, value=value)


@router.get('/restart_project')
def restart_project():  # 获取LAN的 host 信息
    os_type = get_os_type()
    if os_type == 'Windows':
        restart_script()
    elif os_type == 'MacOS':
        restart_script()
    elif os_type == 'Android':
        restart_script()
    value = '--不可能看到这句话出现在任何地方的--#_*0_0O_o'
    return response_with(resp.SUCCESS_200, value=value)  # 理论上执行到不了这一步


# @system_bp.route('/one_click_restart', methods=['GET'])
# def one_click_restart():  # 获取LAN的 host 信息
#     git_pull(REPO_PATH)
#     return response_with(resp.SUCCESS_200, value=value)
