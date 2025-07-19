import os
import re
from collections import Counter


def find_pcaps(files):
    # 通过re正则表达式找到pcap文件
    pcap_mode = '(.*?).p?cap(ng)?$'
    all_pcap = list()
    for file in files:  # 遍历文件夹列表
        if not os.path.isdir(file):
            pcap_find = re.match(pcap_mode, file)
            if pcap_find:  # 在文件夹列表中发现了pcap文件后
                all_pcap.append(file)  # 将它的名字添加到 all_pcap 的列表里
    return all_pcap


def get_host_ip_slow(packets):  #
    # 初始化计数器来统计IP源/目的和ARP源IP地址
    ips_list = Counter()
    arp_sender_ips = Counter()

    for packet in packets:
        if packet.haslayer('IP'):
            ips_list[packet['IP'].src] += 1
            ips_list[packet['IP'].dst] += 1
        if packet.haslayer('ARP'):
            if packet['ARP'].op == 1:
                arp_sender_ips[packet['ARP'].psrc] += 1

    # 计算最常见的发送者和接收者IP地址
    most_common_ip = Counter(ips_list).most_common(1)[0][0]
    most_common_arp = arp_sender_ips.most_common(1)
    if most_common_arp:
        pass
    else:
        return most_common_ip


def ip_collect(*args, ips_list):
    for _ in args:
        if _ not in ips_list:
            ips_list.append(_)
    return ips_list


def ip_stastics(ips_list, hostip):
    lan_ips = list()
    wan_ips = list()
    for _ in ips_list:
        if hostip:
            if _ == hostip:
                pass
            elif '.'.join(_.split('.')[:2]) == '.'.join(hostip.split('.')[:2]):
                lan_ips.append(_)
            else:
                wan_ips.append(_)
        else:
            wan_ips.append(_)
    return (lan_ips, wan_ips)
