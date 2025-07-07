# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: init_project.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 11月 05, 2024 17:45
# ---
import os
import shutil
from api.utils import get_os_type
from api.utils import get_local_ip
import subprocess
import yaml
import re

init_config = {
    'MySQL': {
        'platform': {
            'Android': {
                'host': 'localhost',
                'username': 'admin',
                'password': 'passwd',
                'port': 3306,
                'database': 'test',
                'charset': 'utf8mb4'
            },
            'MacOS': {
                'host': 'localhost',
                'username': 'admin',
                'password': 'passwd',
                'port': 3306,
                'database': 'test',
                'charset': 'utf8mb4'
            },
            'Windows': {
                'host': 'localhost',
                'username': 'admin',
                'password': 'passwd',
                'port': 3306,
                'database': 'test',
                'charset': 'utf8mb4'
            }
        }
    },
    'Redis': {
        'platform': {
            'Android': {
                'host': 'localhost',
                'password': 'passwd',
                'port': 3306,
                'database': 'test',
                'charset': 'utf8mb4',
                'path': ''
            },
            'MacOS': {
                'cli_path': '',
                'conf_path': '',
                'server_path': '',
                'host': 'localhost',
                'password': 'passwd',
                'port': 6379,
                'database': 'test',
                'charset': 'utf8mb4'
            },
            'Windows': {
                'host': 'localhost',
                'password': 'passwd',
                'port': 3306,
                'database': 'test',
                'charset': 'utf8mb4',
                'path': ''
            }
        }
    },
    'server': {
        'host': '127.0.0.1',
        'port': 5055,
        'run_mode': 0
    },
    'Local': {
        'DownloadPath': {
            'MacOS': '/Users/bcy/Downloads',
            'Windows': 'C:/Users/Bcy/Desktop',
            'Android': ''
        }
    },
    'Elasticsearch': {
        'platform': {
            'Android': {
                'host': '127.0.0.1',
                'port': 9200,
                'username': '',
                'password': '',
            },
            'MacOS': {
                'host': '127.0.0.1',
                'port': 9200,
                'username': '',
                'password': '',
            },
            'Windows': {
                'host': '127.0.0.1',
                'port': 9200,
                'username': '',
                'password': '',
            }
        }
    },
    'ngrok': {
        'authtoken': '<authtoken>',
    }
}


def re_config_local_ip():
    """
    重新从bakfile中取原始文件配置现在本地局域网IP 并运行npm run build:prod命令重新生成项目文件。
    """
    # 从config.yaml中读取server host
    with open("config.yaml", "r") as file:  # 打开 YAML 文件
        conf_data = yaml.safe_load(file)  # 加载 YAML 文件内容
    new_local_ip = conf_data.get('server').get('host')
    new_local_ip_port = conf_data.get('server').get('port')

    default_ip_mode = r"\'http://(.*?):5055"

    # 配置vue.config.js
    vite_config_js = open(os.path.join('bakfile', 'vite.config.js.bak'), 'r', encoding='utf-8').read()
    x = re.findall(default_ip_mode, vite_config_js, re.S)[0]  # | re.M
    x = f'http://{x}:5055'
    if 'vite.config.js' in os.listdir(os.path.abspath('')):  # 删除现有的vue.config.js
        print('发现vite.config.js, 准备移除重写!')
        os.remove('vite.config.js')
    with open('vite.config.js', 'w', encoding='utf-8') as vite_conf_js_new:
        vite_conf_js_new.write(vite_config_js.replace(x, f'https://{new_local_ip}:{new_local_ip_port}/'))

    # # 配置.env.development
    # dev_text = open(os.path.join('bakfile', '.env.development.bak'), 'r', encoding='utf-8').read()
    # x = re.findall(default_ip_mode, dev_text, re.S | re.M)[0]
    # x = f'https://{x}:5000/'
    # if '.env.development' in os.listdir(os.path.abspath('')):  # 删除现有的.env.development
    #     os.remove('.env.development')
    # with open('.env.development', 'w', encoding='utf-8') as env_dev:
    #     env_dev.write(dev_text.replace(x, f'http://{new_local_ip}:{new_local_ip_port}/'))

    # # 配置.env.production
    # prod_text = open(os.path.join('bakfile', '.env.production.bak'), 'r', encoding='utf-8').read()
    # x = re.findall(default_ip_mode, prod_text, re.S | re.M)[0]
    # x = f'https://{x}:5000/'
    # if '.env.production' in os.listdir(os.path.abspath('')):  # 删除现有的.env.development
    #     os.remove('.env.production')
    # with open('.env.production', 'w', encoding='utf-8') as env_prod:
    #     env_prod.write(prod_text.replace(x, f'http://{new_local_ip}:{new_local_ip_port}/'))

    # os_type = get_os_type()
    if os_type == 'Android' or os_type == 'Linux' or os_type == 'MacOS':
        subprocess.run(["yarn", "build:prod"], capture_output=False, text=True)
        # subprocess.run(["yarn", "build:prod"], capture_output=False, text=True)
    elif os_type == 'Windows':
        subprocess.run(["yarn", "build:prod"], capture_output=False, text=True, shell=True)
    else:
        print('系统未知，请手动编译项目!')


if __name__ == "__main__":
    os_type = get_os_type()
    print(f"当前系统是 {os_type}")
    ROOT_PATH = os.path.dirname(__file__)

    # 类型为Android时，将./api/app/__init__.py文件删除替换为./api/app/bak/android_termux/__init__.py
    if os_type == 'Android':
        # 删除./api/app/__init__.py
        # print(os.path.join(os.path.dirname(__file__), 'api/app/__init__.py'))
        os.remove(os.path.join(ROOT_PATH, 'api/app/__init__.py'))
        shutil.copyfile(os.path.join(ROOT_PATH, 'api/app/bak/android_termux/__init__.py'),
                        os.path.join(ROOT_PATH, 'api/app/__init__.py'))
    # 类型为Windows时，将./api/app/__init__.py文件删除替换为./api/app/bak/trunk/__init__.py
    if os_type == 'Windows':
        # 删除./api/app/__init__.py
        os.remove(os.path.join(ROOT_PATH, 'api/app/__init__.py'))
        shutil.copyfile(os.path.join(ROOT_PATH, 'api/app/bak/trunk/__init__.py'),
                        os.path.join(ROOT_PATH, 'api/app/__init__.py'))

    if os_type == 'MacOS':
        # 删除./api/app/__init__.py
        os.remove(os.path.join(ROOT_PATH, 'api/app/__init__.py'))
        shutil.copyfile(os.path.join(ROOT_PATH, 'api/app/bak/trunk_mac/__init__.py'),
                        os.path.join(ROOT_PATH, 'api/app/__init__.py'))

    current_local_ip = get_local_ip()  # 获取当前局域网IP
    print(current_local_ip)

    # 项目指定路径下创建初始文件夹供功能使用
    if 'logs' not in os.listdir(os.path.abspath('api')):  # 直接写IP
        os.mkdir(os.path.join(os.path.abspath('api/logs')))
    #
    if 'CodeRepo' not in os.listdir(os.path.abspath('api')):  # 直接写IP
        os.mkdir(os.path.join(os.path.abspath('api/CodeRepo')))

    # 全局配置保存在项目根目录. backend_config.yaml  <-- os_type/current_local_ip
    if 'config.yaml' not in os.listdir(os.path.abspath('')):  # config.yaml初始化
        init_config['server']['host'] = current_local_ip
        with open("config.yaml", "w") as file:  # 打开文件并写入 YAML 格式的内容
            yaml.dump(init_config, file, default_flow_style=False)
        re_config_local_ip()  # 重新配置IP并打包