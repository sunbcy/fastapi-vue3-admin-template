# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: scan_network.py
# @Author: sunbcy
# @Institution: SYLG University, LiaoNing, China
# @E-mail: saintbcy@163.com
# @Time: 9月 25, 2024 07:41
# ---
from scapy.all import ARP, Ether, srp
import ipaddress
import argparse


def scan_network(ip_range):
    # 创建一个以太网广播帧
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # 创建一个ARP请求
    arp = ARP(pdst=ip_range)
    # 将两个层结合在一起
    packet = ether / arp

    # 发送并接收响应
    result = srp(packet, timeout=3, verbose=0)[0]

    # 处理响应
    devices = []
    for sent, received in result:
        # 对于每个响应，添加IP和MAC地址到列表
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices


def get_network_range(ip, prefix_length=24):
    # 创建一个IPv4网络对象
    network = ipaddress.ip_network(f"{ip}/{prefix_length}", strict=False)
    # 获取网络地址
    network_address = network.network_address
    # 返回CIDR表示的网络范围
    return f"{network_address}/{prefix_length}"


def main():
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="")  # Convert an IP address to a network range in CIDR notation.

    # 添加命令行参数
    parser.add_argument('ip', type=str, help='')  # The IP address to convert (e.g., 192.168.18.5)
    parser.add_argument('--prefix', type=int, default=24, help='')  # The prefix length (default: 24)

    # 解析命令行参数
    args = parser.parse_args()

    # 获取并打印网络范围
    ip_range = get_network_range(args.ip, args.prefix)
    online_devices = scan_network(ip_range)
    print(online_devices)


if __name__ == "__main__":
    main()
