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


def validate_ip(ip):
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not (0 <= int(part) <= 255):
                return False
        return True
    except:
        return False


def get_host_ip_slow(packets):
    ips_list = Counter()
    arp_sender_ips = Counter()
    tcp_syn_counter = Counter()

    for packet in packets:
        # IP 统计
        if packet.haslayer('IP'):
            ips_list[packet['IP'].src] += 1
            ips_list[packet['IP'].dst] += 1

            # TCP 连接统计（SYN包发送者）
            if packet.haslayer('TCP') and packet['TCP'].flags & 0x02:
                tcp_syn_counter[packet['IP'].src] += 1

        # ARP 统计
        if packet.haslayer('ARP') and packet['ARP'].op == 1:
            arp_sender_ips[packet['ARP'].psrc] += 1

    # 加权评分系统
    candidates = {}
    for ip in set(ips_list) | set(arp_sender_ips) | set(tcp_syn_counter):
        score = ips_list[ip] * 0.6 + arp_sender_ips[ip] * 0.3 + tcp_syn_counter[ip] * 0.1
        candidates[ip] = score

    return max(candidates, key=candidates.get) if candidates else None


def ip_collect(*args, ips_list):
    for _ in args:
        if _ not in ips_list:
            ips_list.append(_)
    return ips_list


def ip_stastics(ips_list, hostip):
    # 私有IP范围定义
    PRIVATE_IP_RANGES = [
        ("10.0.0.0", 8),
        ("172.16.0.0", 12),
        ("192.168.0.0", 16)
    ]

    lan_ips = set()
    wan_ips = set()

    for ip in ips_list:
        if ip == hostip:
            continue

        is_private = False
        # 检查私有IP范围
        for base, mask_bits in PRIVATE_IP_RANGES:
            base_bytes = list(map(int, base.split('.')))
            ip_bytes = list(map(int, ip.split('.')))

            # 仅比较有效字节
            for i in range(mask_bits // 8):
                if base_bytes[i] != ip_bytes[i]:
                    break
            else:
                is_private = True
                break

        if is_private:
            lan_ips.add(ip)
        else:
            wan_ips.add(ip)

    return list(lan_ips), list(wan_ips)
