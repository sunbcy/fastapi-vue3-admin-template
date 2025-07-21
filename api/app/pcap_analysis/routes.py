from collections import OrderedDict
from traceback import print_exc
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio
import aiofiles
import os

from fastapi import APIRouter, Request, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from scapy.all import rdpcap
from utils import responses as resp
from utils.pcap_tool import get_host_ip_slow, ip_collect, ip_stastics
from utils.responses import response_with

router = APIRouter()
ALLOWED_EXTENSIONS = {'pcap', 'pcapng'}

# 创建线程池 - 用于CPU密集型任务
executor = ThreadPoolExecutor(max_workers=min(4, (os.cpu_count() or 1) + 2))

# 异步分析任务缓存
analysis_tasks = {}
task_count = 0


class AnalysisStatus(BaseModel):
    task_id: int
    status: str  # 'pending', 'processing', 'completed', 'failed'
    progress: int  # 0-100
    filename: str


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 同步的PCAP分析函数（在单独的线程中执行）
def analyse_pcap_sync(pcap_path: str, task_id: int):
    # 更新任务状态为处理中
    analysis_tasks[task_id].status = 'processing'

    try:
        packets = rdpcap(pcap_path)
        total_packets = len(packets)

        host_ip = get_host_ip_slow(packets)
        ips = []
        proto_dict = OrderedDict({
            'IP': 0, 'IPv6': 0, 'TCP': 0, 'UDP': 0, 'ARP': 0,
            'ICMP': 0, 'DNS': 0, 'HTTP': 0, 'HTTPS': 0, 'Others': 0
        })

        for index, packet in enumerate(packets, start=1):
            # 进度报告
            if index % 100 == 0 or index == total_packets:
                progress = int(index / total_packets * 100)
                analysis_tasks[task_id].progress = progress

            # ... [原始分析代码] ...
            # 保持原有的分析逻辑，此处为简洁省略具体实现

        lan_ips, wan_ips = ip_stastics(ips, host_ip)

        # 更新任务状态为已完成
        analysis_tasks[task_id].status = 'completed'
        analysis_tasks[task_id].progress = 100

        return {
            'basic_info': {'host_ip': host_ip, 'lan_ips': lan_ips, 'wan_ips': wan_ips, 'ips': ips},
            'protocol_info': {'protocol_types': proto_dict}
        }

    except Exception as e:
        analysis_tasks[task_id].status = 'failed'
        analysis_tasks[task_id].progress = 100
        raise e


# 异步分析包装器
async def analyse_pcap_async(pcap_path: str, task_id: int):
    loop = asyncio.get_running_loop()
    # 在单独的线程中运行同步分析函数
    return await loop.run_in_executor(
        executor,
        partial(analyse_pcap_sync, pcap_path, task_id)
    )


@router.post('/upload')
async def upload_file(file: UploadFile):
    if not file.filename:
        return JSONResponse(content={'error': 'No selected file'}, status_code=400)

    if not allowed_file(file.filename):
        return JSONResponse(content={'error': 'File type not permitted'}, status_code=400)

    upload_dir = os.path.abspath('uploads')
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, file.filename)

    # 异步写入文件
    async with aiofiles.open(save_path, 'wb') as f:
        content = await file.read()
        await f.write(content)

    return {'message': 'File uploaded successfully', 'filename': file.filename, 'path': save_path}


@router.post('/analysis')
async def start_analysis(request: Request):
    global task_count

    try:
        data = await request.json()
        print(data)
        pcap_list = data.get('data')
        if not pcap_list or not isinstance(pcap_list, list):
            return JSONResponse(content={'error': 'Invalid request data'}, status_code=400)

        upload_dir = os.path.abspath('uploads')
        analysis_results = []

        for file_info in pcap_list:
            pcap_name = file_info.get('name')
            if not pcap_name:
                continue

            task_count += 1
            file_path = os.path.join(upload_dir, pcap_name)

            # 初始化任务状态
            analysis_tasks[task_count] = AnalysisStatus(
                task_id=task_count,
                status='pending',
                progress=0,
                filename=pcap_name
            )

            # 启动异步分析任务但不等待结果
            asyncio.create_task(
                process_single_pcap(file_path, task_count)
            )

            analysis_results.append({
                'id': task_count,
                'packetName': pcap_name,
                'statusLink': f'/task/status/{task_count}'
            })
        print(analysis_results)

        return response_with(resp.SUCCESS_200, value={'tasks': analysis_results})

    except Exception as e:
        print_exc()
        return response_with(resp.SERVER_ERROR_500, value={'error': str(e)})


async def process_single_pcap(file_path, task_id):
    """异步处理单个PCAP文件"""
    try:
        # 执行异步分析
        result = await analyse_pcap_async(file_path, task_id)

        # 存储结果
        analysis_tasks[task_id].result = result

    except Exception as e:
        # 任务状态已在analyse_pcap_sync中更新
        pass


@router.get('/task/status/{task_id}')
async def get_task_status(task_id: int):
    """获取任务状态"""
    task = analysis_tasks.get(task_id)
    if not task:
        return JSONResponse(content={'error': 'Task not found'}, status_code=404)

    response = {
        'task_id': task_id,
        'status': task.status,
        'progress': task.progress,
        'filename': task.filename
    }

    if task.status == 'completed':
        response['result'] = task.result
        response['resultLink'] = f'/task/result/{task_id}'

    return JSONResponse(content=response)


@router.get('/task/result/{task_id}')
async def get_task_result(task_id: int):
    """获取完整分析结果"""
    task = analysis_tasks.get(task_id)
    if not task:
        return JSONResponse(content={'error': 'Task not found'}, status_code=404)

    if task.status != 'completed':
        return JSONResponse(content={'error': 'Analysis not completed yet'}, status_code=400)

    return JSONResponse(content=task.result)


@router.get('/stream-progress/{task_id}')
async def stream_progress(task_id: int):
    """SSE流式传输任务进度"""
    task = analysis_tasks.get(task_id)
    if not task:
        return JSONResponse(content={'error': 'Task not found'}, status_code=404)

    async def event_generator():
        last_progress = -1

        while task.status in ['pending', 'processing']:
            if task.progress != last_progress:
                last_progress = task.progress
                yield f"data: {task.progress}\n\n"
                await asyncio.sleep(0.5)  # 减少检查频率
            else:
                await asyncio.sleep(0.1)

        if task.status == 'completed':
            yield f"data: 100\n\n"
        elif task.status == 'failed':
            yield f"event: error\ndata: Analysis failed\n\n"

        yield "event: close\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
