# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
import json

import aiohttp
# from app import db
# from app.liepin.models import JobRequest, JobRecommendation
# from app.liepin.schema import jobRecommendationScheme
from fastapi import APIRouter
from lxml import etree
from pydantic import BaseModel
from utils import check_proxy
from utils import get_os_type
from utils import load_server_config
from utils import responses as resp
from utils.responses import response_with

router = APIRouter()


def _parse_cookie_string(cookie_str: str) -> dict:
    """将 'a=1; b=2' 形式的 cookie 字符串解析为字典。"""
    cookies = {}
    for pair in cookie_str.split(';'):
        pair = pair.strip()
        if not pair or '=' not in pair:
            continue
        key, _, value = pair.partition('=')
        cookies[key.strip()] = value.strip()
    return cookies


class JobDetail(BaseModel):
    # jobUrl: str
    payload: dict


class JobReq(BaseModel):
    city: str
    dq: str
    currentPage: int
    key: str
    workYearCode: int


class LiepinSearchJob:
    """猎聘网搜索职位接口-- from web
    """
    def __init__(self, payload):
        super(LiepinSearchJob, self).__init__()
        self.url = 'https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job'  # %E5%B5%8C%E5%85%A5%E5%BC%8F
        self.X_Fscp_Std_Info = {"client_id": "40108"}
        self.cookies = self._load_cookies()
        self.headers = {
            'X-Fscp-Version': '1.1',
            'X-Fscp-Std-Info': json.dumps(self.X_Fscp_Std_Info),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'X-Fscp-Bi-Stat': '{"location": ""}',
            'Content-Type': 'application/json;charset=UTF-8;',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Client-Type': 'web',
            'X-Fscp-Trace-Id': 'e1929537-67e9-497a-9287-862c1af97549'
        }
        self.mainSearchPcConditionForm = payload  # {'city': '410', 'dq': '410', 'currentPage': 0, 'key': 'python',
        # 'workYearCode': '0'}
        self.data = {'mainSearchPcConditionForm': '%s' % self.mainSearchPcConditionForm}
        self.form_data = {'data': self.data}
        self.payload = {"data": {"mainSearchPcConditionForm": payload}}
        # {"city": "410", "dq": "410", "currentPage": 0, "pageSize": 40, "key": "小米开发", "suggestTag": "", "workYearCode": "0"}

    @staticmethod
    def _load_cookies():
        """从 config.yaml 读取猎聘登录态 cookie（登录后在浏览器开发者工具复制）。

        支持两种写法：
          1) cookies: "a=1; b=2"  (浏览器复制的 cookie 字符串)
          2) cookies: {a: "1", b: "2"}  (yaml 字典)
        """
        raw = load_server_config().get('cookies', '')
        if not raw:
            print('警告: 未配置 Liepin.cookies，接口将返回 401，请在 config.yaml 中填写登录态 cookie')
            return {}
        if isinstance(raw, dict):
            return {str(k): str(v) for k, v in raw.items()}
        return _parse_cookie_string(str(raw))

    async def get_liepin_searchjobs(self):
        print(f"当前访问第 {self.payload['data']['mainSearchPcConditionForm']['currentPage'] + 1} 页")
        async with aiohttp.ClientSession() as session:
            if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                async with session.post(self.url,
                                        headers=self.headers,
                                        cookies=self.cookies,
                                        json=self.payload,
                                        proxy=check_proxy()['http']) as response:
                    r_text = await response.text()
            else:
                async with session.post(self.url,
                                        headers=self.headers,
                                        cookies=self.cookies,
                                        json=self.payload) as response:
                    r_text = await response.text()
        # print(f'状态码: <{r.status_code}>')
        result_ret = json.loads(r_text)  # r.text  #
        print(result_ret)
        pagination = result_ret['data']['pagination']
        current_page = pagination['currentPage']
        total_page = pagination['totalPage']
        # hasNext = pagination['hasNext'] # 此参数无用
        while current_page < total_page:
            self.payload['data']['mainSearchPcConditionForm']['currentPage'] += 1
            print(f"当前访问第 {self.payload['data']['mainSearchPcConditionForm']['currentPage'] + 1} 页")
            async with aiohttp.ClientSession() as session:
                if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                    async with session.post(self.url,
                                            headers=self.headers,
                                            cookies=self.cookies,
                                            json=self.payload,
                                            proxy=check_proxy()['http']) as response:
                        r_text = await response.text()
                else:
                    async with session.post(self.url,
                                            headers=self.headers,
                                            cookies=self.cookies,
                                            json=self.payload) as response:
                        r_text = await response.text()
            # print(f'状态码: <{r.status_code}>')
            result_next = json.loads(r_text)
            print(result_next)
            result_ret['data']['data']['jobCardList'] += (result_next['data']['data']['jobCardList'] if
                                                          'jobCardList' in result_next['data']['data'] else
                                                          [])
            pagination = result_next['data']['pagination']
            current_page = pagination['currentPage']
            total_page = pagination['totalPage']
        jobs = []
        try:
            job_card_list = result_ret['data']['data']['jobCardList']
            for i in job_card_list:
                job = i['job']
                recruiter = i['recruiter']
                comp = i['comp']
                job_cnt = {
                    'dataInfo': i['dataInfo'],
                    'dataParams': str(i['dataParams']),
                    'job_title': job['title'],
                    'job_salary': job['salary'],
                    'job_dq': job['dq'],
                    'job_requireWorkYears': job['requireWorkYears'] if 'requireWorkYears' in job else '',
                    'job_requireEduLevel': job['requireEduLevel'] if 'requireEduLevel' in job else '',
                    'job_labels': str(job['labels']),
                    'job_link': job['link'],
                    'jobId': job['jobId'],
                    'topJob': job['topJob'],
                    'job_advViewFlag': job['advViewFlag'],
                    'job_dataPromId': job['dataPromId'],
                    'recruiterName': recruiter['recruiterName'] if 'recruiterName' in recruiter else '',
                    'recruiterTitle': recruiter['recruiterTitle'] if 'recruiterTitle' in recruiter else '',
                    'recruiter_imId': recruiter['imId'] if 'imId' in recruiter else '',
                    'recruiter_imUserType': recruiter['imUserType'] if 'imUserType' in recruiter else '',
                    'recruiter_chatted': recruiter['chatted'] if 'chatted' in recruiter else '',
                    'recruiterId': recruiter['recruiterId'] if 'recruiterId' in recruiter else '',
                    'recruiterPhoto': recruiter['recruiterPhoto'] if 'recruiterPhoto' in recruiter else '',
                    'compId': str(comp['compId']) if 'compId' in comp else '',
                    'compName': comp['compName'],
                    'compScale': comp['compScale'] if 'compScale' in comp else '',
                    'compStage': comp['compStage'] if 'compStage' in comp else '',
                    'compIndustry': comp['compIndustry'] if 'compIndustry' in comp else '',
                    'compLogo': comp['compLogo'] if 'compLogo' in comp else '',
                    'comp_link': comp['link'] if 'link' in comp else '',
                    'jobKind': job['jobKind'],
                    'job_refreshTime': job['refreshTime'],
                    'job_intro_content': '',
                    'job_origin': '猎聘',
                    'username': '',
                    'usermail': ''
                }
                # print(i)  # 打印job card 信息
                # if get_os_type() in ('Windows', 'MacOS'):
                #     if not self.jobrecommend_oper.query_jobId(jobId=job['jobId']):
                #         self.jobrecommend_oper.insert_job(**jobCnt)
                # else:  # 如果是Android系统，目前无法直接使用机器上的数据库，需要做检测，做调起。
                #     pass
                # 返回信息
                ret_info = {
                    "Job": {
                        "job_title": job['title'],
                        "job_labels": str(job['labels']),
                        "job_requireEduLevel": job['requireEduLevel'] if 'requireEduLevel' in job else '',
                        "job_salary": job['salary'],
                        "job_dq": job['dq'],
                        "job_requireWorkYears": job['requireWorkYears'] if 'requireWorkYears' in job else '',
                        "job_link": job['link'],
                    },
                    "Recruiter": {
                        "recruiterTitle": recruiter['recruiterTitle'] if 'recruiterTitle' in recruiter else '',
                        "recruiterName": recruiter['recruiterName'] if 'recruiterName' in recruiter else ''
                    },
                    "Company": {
                        "compName": comp['compName'],
                        "compIndustry": comp['compIndustry'] if 'compIndustry' in comp else '',
                        "compScale": comp['compScale'] if 'compScale' in comp else '',
                        "compStage": comp['compStage'] if 'compStage' in comp else '',
                        "comp_link": comp['link'] if 'link' in comp else ''
                    }
                }
                jobs.append(ret_info)
        except Exception as e:
            if 'KeyError' in str(e.args) and 'jobCardList' in str(e.args):
                print('job not found!', result_ret['data']['data'])
        finally:
            return jobs

    async def get_job_detail_infos(self, job_link):
        print('【访问】 {job_link}'.format(job_link=job_link))
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        async with aiohttp.ClientSession() as session:
            if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                async with session.get(job_link,
                                       headers=self.headers,
                                       proxy=check_proxy()['http']
                                       ) as response:
                    r_text = await response.text()
            else:
                async with session.get(job_link,
                                       headers=self.headers
                                       ) as response:
                    r_text = await response.text()
        html = etree.HTML(r_text)
        try:
            web_title = html.xpath('//head/title/text()')[0]
            job_id = job_link.split('/')[-1].split('.')[0]
            job_title = html.xpath('//div[@class="job-apply-content"]//span[@class="name ellipsis-1"]/text()')[0]
            job_salary = html.xpath('//div[@class="job-apply-content"]//span[@class="salary"]/text()')[0]
            job_properties = html.xpath('//div[@class="job-apply-content"]//div[@class="job-properties"]/span/text()')
            company_url = html.xpath('//main//content//div[@class="title-box"]//span/a/@href')[0]
            company_id = company_url.split('/')[-2]
            job_intro_tag = html.xpath('//main//content//section[@class="job-intro-container"]//ul/li/text()')
            job_tags = str(tuple(job_properties + job_intro_tag))
        except Exception:
            job_tags = ''

        try:
            job_intro_content = html.xpath('//main//content//dd[@data-selector="job-intro-content"]//text()')[0]
        except IndexError as e:
            job_intro_content = 'test'
            print('Index Error !!!!!估计被猎聘安全中心发现了!!!!!!quit~~')

        try:
            company_intro = html.xpath(
                '//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')[0]
        except IndexError as e:
            company_intro = html.xpath(
                '//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')
            if not company_intro:
                company_intro = ''
        # print(f"company_intro为{company_intro}")

        try:
            company_logo = html.xpath(
                '//main//aside//div[@class="company-info-container"]//img')[0].get('src')
            company_name = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="name ellipsis-1"]/text()')[0]
            company_industry = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="company-other"]//span[@class="text"]')[0].text
            company_stage = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="company-other"]//span[@class="text"]')[1].text
            company_scale = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="company-other"]//span[@class="text"]')[2].text
            company_addr = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="company-other"]//span[@class="text"]')[3].text
            company_register_time = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="register-info"]//span[@class="text"]')[0].text
            company_register_money = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="register-info"]//span[@class="text"]')[1].text
            company_register_include = html.xpath(
                '//main//aside//div[@class="company-info-container"]//div[@class="register-info"]//span[@class="text"]')[2].text
            company_info = (f'公司信息:\n'
                            f'公司Logo: {company_logo}\n'
                            f'公司名字: {company_name}\n'
                            f'企业行业: {company_industry}\n'
                            f'融资阶段: {company_stage}\n'
                            f'人数规模: {company_scale}\n'
                            f'职位地址: {company_addr}\n'
                            f'注册时间: {company_register_time}\n'
                            f'注册资本: {company_register_money}\n'
                            f'经营范围: {company_register_include}\n')
        except Exception as e:
            company_info = ''
        job_detail = {'job_tags': job_tags,
                      'job_intro_content': job_intro_content,
                      'company_intro': company_intro,
                      'company_info': company_info}
        print(job_detail)
        return job_detail


@router.post('/get_jobs')
async def get_jobs_from_liepinsearch(job_req: JobReq):
    """
    根据前端筛选条件获取职位
    """
    liepin_job_res = LiepinSearchJob(payload=job_req.dict())
    liepin_job_res = await liepin_job_res.get_liepin_searchjobs()  # liepin API返回的职位
    try:
        value = {'searchResults': [{'id': liepin_job_res.index(j) + 1,
                                    'job_title': j['Job']['job_title'],
                                    'job_dq': j['Job']['job_dq'],
                                    'job_salary': j['Job']['job_salary'],
                                    'job_link': j['Job']['job_link'],
                                    'job_requireWorkYears': j['Job']['job_requireWorkYears'],
                                    'job_requireEduLevel': j['Job']['job_requireEduLevel'],
                                    'job_labels': j['Job']['job_labels'],
                                    'compName': j['Company']['compName'],
                                    'compIndustry': j['Company']['compIndustry'],
                                    'compScale': j['Company']['compScale'],
                                    'comp_link': j['Company']['comp_link']} for j in liepin_job_res]}
        return response_with(resp.SUCCESS_200, value=value)  # page_links
    except Exception as e:
        value = {'searchResults': []}
        return response_with(resp.NOT_FOUND_HANDLER_404, value=value)


@router.post('/getJobDetails')
async def getJobDetails(job_detail: JobDetail):
    """根据job URL 返回 job detail
    """
    job_url = job_detail.payload.get('jobUrl')  # 前端请求的参数
    liepin_job_res = LiepinSearchJob(payload=job_detail.payload)
    job_detail_result = await liepin_job_res.get_job_detail_infos(job_url)
    try:
        value = {'searchResults': job_detail_result}
        return response_with(resp.SUCCESS_200, value=value)
    except Exception as e:
        value = {'searchResults': {}}
        return response_with(resp.NOT_FOUND_HANDLER_404, value=value)


# @router.get('/get_job_num')
# def get_job_num():
#     try:
#         jobrecommend_oper = jobRecommendationScheme()
#         job_num = jobrecommend_oper.queryJobNum()
#         value = {'searchResults': str(job_num)}
#     except Exception as e:
#         value = {'searchResults': 0}
#     return response_with(resp.SUCCESS_200, value=value)


# @router.get('/get_comp_num')
# def get_comp_num():
#     try:
#         jobrecommend_oper = jobRecommendationScheme()
#         compNum = jobrecommend_oper.query_distinct_column_count('compName')  # 根据此列名筛选出了公司数目
#         value = {'searchResults': str(compNum)}
#     except Exception as e:
#         value = {'searchResults': 0}
#     return response_with(resp.SUCCESS_200, value=value)


@router.get('/get_top_ten_industries')
def get_top_ten_industries():
    top_ten_industries_saved = ({'value': 584, 'name': '互联网'},
                                {'value': 535, 'name': '计算机软件'},
                                {'value': 268, 'name': '电子商务'},
                                {'value': 171, 'name': '电子/半导体/集成电路'},
                                {'value': 151, 'name': '通信设备'},
                                {'value': 133, 'name': 'IT服务'},
                                {'value': 122, 'name': '批发/零售'},
                                {'value': 111, 'name': '贸易/进出口'},
                                {'value': 106, 'name': '专业技术服务'},
                                {'value': 97, 'name': '机械/设备'})
    if get_os_type() in ('Windows', 'MacOS'):
        try:
            jobrecommend_oper = jobRecommendationScheme()
            top_ten_industries = jobrecommend_oper.get_top_ten_industries()
            if not top_ten_industries:  # 如果数据库返回为空
                top_ten_industries = top_ten_industries_saved
        except Exception as e:
            top_ten_industries = top_ten_industries_saved
    else:  # Android
        top_ten_industries = top_ten_industries_saved
    # print(top_ten_industries)
    value = {'searchResults': top_ten_industries}
    return response_with(resp.SUCCESS_200, value=value)
