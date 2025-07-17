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
from utils import responses as resp
from utils.responses import response_with

router = APIRouter()


class JobDetail(BaseModel):
    jobUrl: str
    payload: dict


class JobReq(BaseModel):
    city: str
    dq: str
    currentPage: int
    key: str
    workYearCode: int


class liepin_searchjob:
    """猎聘网搜索职位接口-- from web
    """
    def __init__(self, payload):
        super(liepin_searchjob, self).__init__()
        self.url = 'https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job'  # %E5%B5%8C%E5%85%A5%E5%BC%8F
        self.X_Fscp_Std_Info = {"client_id": "40108"}
        self.cookies = {
            'inited_user': '01316af02afca9c8e3fe318c5931025c',
            '_ga': 'GA1.1.1974346437.1709541959',
            'need_bind_tel': 'false',
            'new_user': 'false',
            'c_flag': 'ffb65a1cfb07b7eb657371e4a0339a01',
            '__uuid': '1725036287314.61',
            '__gc_id': 'a0e17efbde5340369cd236a869e9aafa',
            'imId': 'c1affafc1a79ee733ee4dc6efa402073',
            'imId_0': 'c1affafc1a79ee733ee4dc6efa402073',
            'imClientId': 'c1affafc1a79ee733f1f8a514ea150a7',
            'imClientId_0': 'c1affafc1a79ee733f1f8a514ea150a7',
            'XSRF-TOKEN': 'IbTyT67ZSKix3A-vyCCzjw',
            'Hm_lvt_a2647413544f5a04f00da7eee0d5e200': '1725036325,1726317142',
            'HMACCOUNT': 'A9C94FD1A0D780E7',
            '__tlog': '1726317141989.57%7C00000000%7C00000000%7C00000000%7C00000000',
            'hpo_role-sec_project': 'sec_project_liepin',
            'hpo_sec_tenant': '0',
            'user_roles': '0',
            'user_photo': '5f8fa3a78dbe6273dcf85e2608u.png',
            'user_name': '%E5%8D%9E%E6%99%A8%E9%98%B3',
            'imApp_0': '1',
            'UniqueKey': '418ec1ca83a46a561a667e00ad0d9493',
            'liepin_login_valid': '0',
            'lt_auth': '7uwDa3EDxgj67XiI2Gpe46cbjImpA2TK8y8FhU0H1tXuDaLr4PvrQQqFqrEAxAMhxBp9ccULNrL4Pez5yXdL6UAUwGmglICxv%2F6k034HUeVsJ8W2vezHg%2FXUQp4hk0AA8nJbpEIL%2BVzO',
            'access_system': 'C',
            'acw_tc': '1a0c638417268470430241930e00455665002370612273c817cf13b86ecdd5',
            'inited_user': '01316af02afca9c8e3fe318c5931025c',
            'Hm_lpvt_a2647413544f5a04f00da7eee0d5e200': '1726848033',
            '_ga_54YTJKWN86': 'GS1.1.1726843970.34.1.1726848032.0.0.0',
            'fe_im_connectJson_0': '%7B%220_418ec1ca83a46a561a667e00ad0d9493%22%3A%7B%22socketConnect%22%3A%221%22%2C%22connectDomain%22%3A%22liepin.com%22%7D%7D',
            'fe_im_opened_pages': '1726323101391_1726848033747_1726848006547',
            'fe_im_socketSequence_new_0': '8_7_8',
            '__session_seq': '26',
            '__tlg_event_seq': '330',
        }
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
        self.mainSearchPcConditionForm = payload  # {'city': '410', 'dq': '410', 'currentPage': 0, 'key': 'python', 'workYearCode': '0'}
        self.data = {'mainSearchPcConditionForm': '%s' % self.mainSearchPcConditionForm}
        self.form_data = {'data': self.data}
        self.payload = {"data": {"mainSearchPcConditionForm": payload}}  # {"city": "410", "dq": "410", "currentPage": 0, "pageSize": 40, "key": "小米开发", "suggestTag": "", "workYearCode": "0"}
        self.proxy = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890'
        }
        # self.jobrecommend_oper = jobRecommendationScheme()  # 生成职位推荐对象

    async def get_liepin_searchjobs(self):
        print(f"当前访问第 {self.payload['data']['mainSearchPcConditionForm']['currentPage'] + 1} 页")
        async with aiohttp.ClientSession() as session:
            if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                async with session.post(self.url, headers=self.headers, cookies=self.cookies, json=self.payload, proxy=check_proxy()['http']) as response:
                    r_text = await response.text()
            else:
                async with session.post(self.url, headers=self.headers, cookies=self.cookies, json=self.payload) as response:
                    r_text = await response.text()
        # print(f'状态码: <{r.status_code}>')
        result_ret = json.loads(r_text)  # r.text  #
        print(result_ret)
        pagination = result_ret['data']['pagination']
        currentPage = pagination['currentPage']
        totalPage = pagination['totalPage']
        # hasNext = pagination['hasNext'] # 此参数无用
        while currentPage < totalPage:
            self.payload['data']['mainSearchPcConditionForm']['currentPage'] += 1
            print(f"当前访问第 {self.payload['data']['mainSearchPcConditionForm']['currentPage'] + 1} 页")
            async with aiohttp.ClientSession() as session:
                if check_proxy():  # 如果是安卓情况下,check_proxy()可能检测不到代理端口故此多个判断.
                    async with session.post(self.url, headers=self.headers, cookies=self.cookies, json=self.payload, proxy=check_proxy()['http']) as response:
                        r_text = await response.text()
                else:
                    async with session.post(self.url, headers=self.headers, cookies=self.cookies, json=self.payload) as response:
                        r_text = await response.text()
            # print(f'状态码: <{r.status_code}>')
            result_next = json.loads(r_text)
            print(result_next)
            result_ret['data']['data']['jobCardList'] += (result_next['data']['data']['jobCardList'] if 'jobCardList' in result_next['data']['data'] else [])
            pagination = result_next['data']['pagination']
            currentPage = pagination['currentPage']
            totalPage = pagination['totalPage']
        jobs = []
        try:
            jobCardList = result_ret['data']['data']['jobCardList']
            for i in jobCardList:
                job = i['job']
                recruiter = i['recruiter']
                comp = i['comp']
                jobCnt = {
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
                async with session.get(job_link, headers=self.headers, proxy=check_proxy()['http']) as response:
                    r_text = await response.text()
            else:
                async with session.get(job_link, headers=self.headers) as response:
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
            if (not company_intro):
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
            company_info = f'公司信息:\n公司Logo: {company_logo}\n公司名字: {company_name}\n企业行业: {company_industry}\n融资阶段: {company_stage}\n人数规模: {company_scale}\n职位地址: {company_addr}\n注册时间: {company_register_time}\n注册资本: {company_register_money}\n经营范围: {company_register_include}\n'
        except Exception as e:
            company_info = ''
        job_detail = {'job_tags': job_tags, 'job_intro_content': job_intro_content, 'company_intro': company_intro, 'company_info': company_info}
        print(job_detail)
        return job_detail


@router.post('/get_jobs')
async def get_jobs_from_liepinsearch(job_req: JobReq):
    """
    根据前端筛选条件获取职位
    """
    liepin_job_res = liepin_searchjob(payload=job_req.dict())
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
async def getJobDetails(jobDetail: JobDetail):
    """根据job URL 返回 job detail
    """
    jobUrl = jobDetail.jobUrl  # 前端请求的参数
    liepin_job_res = liepin_searchjob(payload=jobDetail.payload)
    jobDetailResult = await liepin_job_res.get_job_detail_infos(jobUrl)
    try:
        value = {'searchResults': jobDetailResult}
        return response_with(resp.SUCCESS_200, value=value)
    except Exception as e:
        value = {'searchResults': {}}
        return response_with(resp.NOT_FOUND_HANDLER_404, value=value)


@router.get('/get_job_num')
def get_job_num():
    try:
        jobrecommend_oper = jobRecommendationScheme()
        jobNum = jobrecommend_oper.queryJobNum()
        value = {'searchResults': str(jobNum)}
    except Exception as e:
        value = {'searchResults': 0}
    return response_with(resp.SUCCESS_200, value=value)


@router.get('/get_comp_num')
def get_comp_num():
    try:
        jobrecommend_oper = jobRecommendationScheme()
        compNum = jobrecommend_oper.query_distinct_column_count('compName')  # 根据此列名筛选出了公司数目
        value = {'searchResults': str(compNum)}
    except Exception as e:
        value = {'searchResults': 0}
    return response_with(resp.SUCCESS_200, value=value)


@router.get('/get_top_ten_industries')
def get_top_ten_industries():
    top_ten_industries_saved = [{'value': 584, 'name': '互联网'}, {'value': 535, 'name': '计算机软件'},
                          {'value': 268, 'name': '电子商务'}, {'value': 171, 'name': '电子/半导体/集成电路'},
                          {'value': 151, 'name': '通信设备'}, {'value': 133, 'name': 'IT服务'},
                          {'value': 122, 'name': '批发/零售'}, {'value': 111, 'name': '贸易/进出口'},
                          {'value': 106, 'name': '专业技术服务'}, {'value': 97, 'name': '机械/设备'}]
    if get_os_type() in ['Windows', 'MacOS']:
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
