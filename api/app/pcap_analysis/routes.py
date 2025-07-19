from collections import OrderedDict
from traceback import print_exc

from fastapi import APIRouter
from fastapi import Request
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# from werkzeug.utils import secure_filename
from scapy.all import rdpcap
from scapy_ssl_tls.ssl_tls import *
from utils import responses as resp
from utils.pcap_tool import get_host_ip_slow, ip_collect, ip_stastics
from utils.responses import response_with

router = APIRouter()
# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'pcap', 'pcapng'}  # , 'png', 'jpg', 'jpeg', 'gif'}


class FormData(BaseModel):
    file: Optional[UploadFile] = None


# 用于检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def analyse_pcap(pcap_file):
    pcap_name = pcap_file.split('.')[0]
    print(f'分析 {pcap_name} 中!')
    packets = rdpcap(pcap_file)

    host_ip = get_host_ip_slow(packets)  # 返回数据包本机IP
    """
    慢方法,同时更精确,基于统计和假设 这是因为pcap文件可能包含多个子网的流量或者来自多个主机的流量。
    若要提高结果的准确性，可以进一步分析pcap文件中的流量模式，比如：
    - 识别哪个IP地址与你的内网范围或已知的网络配置相匹配。
    - 查看哪个IP拥有最多的开放连接或会话初始。在某些情况下，还可以结合时间戳和数据包大小等其他元数据来协助判断。
    如果你有关于网络配置的额外信息，或者知道某些特定的通信模式，这可能会帮助你对本机IP进行更准确的推断。
    始终需要考虑网络的具体环境和场景，以及流量可能反映的其他特点来综合判断。 
    from gpt-4
    """
    ips = list()
    proto_dict = OrderedDict()
    proto_dict['IP'] = 0
    proto_dict['IPv6'] = 0
    proto_dict['TCP'] = 0
    proto_dict['UDP'] = 0
    proto_dict['ARP'] = 0
    proto_dict['ICMP'] = 0
    proto_dict['DNS'] = 0
    proto_dict['HTTP'] = 0
    proto_dict['HTTPS'] = 0
    proto_dict['Others'] = 0
    for index, packet in enumerate(packets, start=1):
        if packet.haslayer('IP'):  # 有IP层
            proto_dict['IP'] += 1
            src_ip = packet['IP'].src
            dst_ip = packet['IP'].dst
            ips = ip_collect(src_ip, dst_ip, ips_list=ips)  # 收集IP
            if packet.haslayer('TCP') or packet.haslayer('UDP'):
                src_port = packet.sport
                dst_port = packet.dport
            # print(f'{index} {src_ip}:{src_port} -> {dst_ip}:{dst_port}')
        elif packet.haslayer('IPv6'):
            proto_dict['IPv6'] += 1
        if packet.haslayer('ARP'):
            proto_dict['ARP'] += 1
        elif packet.haslayer('ICMP'):
            proto_dict['ICMP'] += 1
        elif packet.haslayer('DNS'):
            proto_dict['DNS'] += 1
            # query_name = packet['DNS'].qname
            # print(f'{packet}')
            # packet.show()
            # print(f'{query_name}')
        elif packet.haslayer('TCP'):  # packet.haslayer('Raw') and
            proto_dict['TCP'] += 1
            tcp = packet.getlayer('TCP')

            dport = tcp.dport
            sport = tcp.sport
            if dport == 80 or sport == 80:
                proto_dict['HTTP'] += 1
            elif dport == 443 or sport == 443:
                proto_dict['HTTPS'] += 1
            else:
                proto_dict['Others'] += 1
            try:  # 尝试对payload解码
                payload = tcp.load  # packet['TCP']
                if payload.decode():
                    if 'HTTP' in payload.decode():  # HTTP层
                        headers = payload.decode().split("\r\n")  # 分离头部。
                        for field in headers:
                            # 筛选出 Host 字段。
                            if field.startswith('Host:'):
                                host = field.split(': ')[1]
                                print(f'Host: {host}')
                        # break
            except Exception:
                pass
        elif packet.haslayer('UDP'):
            proto_dict['UDP'] += 1
            udp = packet.getlayer('UDP')
            dport = udp.dport
            sport = udp.sport
            if dport == 5353 or sport == 5353:
                proto_dict['DNS'] += 1
            else:
                proto_dict['Others'] += 1
        elif packet.haslayer('ICMPv6ND_NS'):  # ?
            proto_dict['ICMP'] += 1
        else:
            proto_dict['Others'] += 1

            # print(payload)
            # packet.show()
            # break
        # break
        # if packet.haslayer('IP'):
        #     print(packet)

    lan_ips, wan_ips = ip_stastics(ips, host_ip)

    return {
        'basic_info': {
            'host_ip': host_ip,
            'lan_ips': lan_ips,
            'wan_ips': wan_ips,
            'ips': ips,
        },
        'protocol_info': {
            'protocol_types': proto_dict,

        },
        # 'stream_info': {
        #     'pcap_size': pcap_size
        # },
        # 'other': other
    }


@router.post('/upload')
async def upload_file(request: Request):
    # 获取表单数据
    form_data = await request.form()

    # 检查是否有文件在请求中
    if 'file' not in form_data:
        return JSONResponse(content={'error': 'No file part in the request'}, status_code=400)

    file = form_data['file']
    # 如果用户没有选择文件，浏览器也可能提交一个没有文件名的空表单字段
    if file.filename == '':
        return JSONResponse(content={'error': 'No selected file'}, status_code=400)

    if file and allowed_file(file.filename):
        # 使用 Werkzeug 提供的 secure_filename 方法增强文件名的安全性
        # filename = secure_filename(file.filename)
        filename = file.filename
        save_path = os.path.abspath(f'uploads/{filename}')
        # file.save(save_path)
        # 保存文件
        with open(save_path, "wb") as f:
            f.write(await file.read())
        return JSONResponse(content={'message': 'File uploaded successfully', 'filename': filename}, status_code=200)
    else:
        return JSONResponse(content={'error': 'File type not permitted'}, status_code=400)


@router.api_route('/analysis', methods=['GET', 'POST'])
async def analyse_file(request: Request):
    data = await request.json()  #
    pcap_list = data.get('data')
    upload_dir = os.path.abspath('uploads')
    all_ret_info = []
    format_ret = {}
    try:
        for index, _ in enumerate(pcap_list, start=1):
            pcap_name = _.get('name')
            real_pcap = '/'.join((upload_dir, pcap_name))
            ret_info = analyse_pcap(real_pcap)
            all_ret_info.append({'id': index,
                                 'packetName': pcap_name,
                                 'resultLink': '/result/' + str(index),
                                 'ret_info': ret_info})
        format_ret = {'data': all_ret_info}
        return response_with(resp.SUCCESS_200, value=format_ret)
    except Exception as e:
        print_exc()
        value = {'data': []}
        return response_with(resp.SERVER_ERROR_500, value=value)
