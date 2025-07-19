#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/14 23:29
# @Author  : sunbcy
# @File    : api_test.py
# @Software: PyCharm
import json
import socket
import urllib.request

from lxml import etree
import aiohttp
import asyncio
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, func
# from sqlalchemy.orm import sessionmaker, declarative_base


# class Config(object):
#     SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://bcy:12345678@127.0.0.1:3306/test_20240403'  # 'sqlite:///books.db'  test_20240320  web_analysis
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
# Base = declarative_base()  # 建立 sql rom基类
# Session = sessionmaker(bind=engine)
#
# db = SQLAlchemy()


# class JobRequest(db.Model):
#     """建工作需求单
#
#     Args:
#         Base (_type_): _description_
#     """
#     # 指定映射表名
#     __tablename__ = 'job_request'
#
#     # ID设置为主键
#     id = db.Column(db.Integer,
#                    primary_key=True)  # autoincrement=True, index=True, nullable=False, unique=True, default=18
#     username = db.Column(db.String(32), index=True)
#     usermail = db.Column(db.String(50))
#     city = db.Column(db.String(32))
#     dq = db.Column(db.String(32))
#     pubTime = db.Column(db.String(50))
#     currentPage = db.Column(db.Integer)
#     pageSize = db.Column(db.Integer)
#     Key = db.Column(db.String(32))
#     suggestTag = db.Column(db.String(50))
#     workYearCode = db.Column(db.String(10))
#     compId = db.Column(db.String(20))
#     compName = db.Column(db.String(50))
#     compTag = db.Column(db.String(32))
#     industry = db.Column(db.String(50))
#     salary = db.Column(db.String(10))
#     jobKind = db.Column(db.String(5))
#     compScale = db.Column(db.String(32))
#     compKind = db.Column(db.String(32))
#     compStage = db.Column(db.String(32))
#     eduLevel = db.Column(db.String(32))
#     ctime = db.Column(db.DateTime(), server_default=db.func.now())
#     mtime = db.Column(db.DateTime(), onupdate=db.func.now())
#
#     __table_args__ = (
#         db.UniqueConstraint('id', 'username', name='uix_id_username'),
#     )
#
#     def __init__(self, username, usermail, city, dq, pubTime, currentPage, \
#                  pageSize, Key, suggestTag, workYearCode, compId, compName, compTag, \
#                  industry, salary, jobKind, compScale, compKind, compStage, eduLevel):
#         self.username = username
#         self.usermail = usermail
#         self.city = city
#         self.dq = dq
#         self.city = city
#         self.pubTime = pubTime
#         self.currentPage = currentPage
#         self.pageSize = pageSize
#         self.Key = Key
#         self.suggestTag = suggestTag
#         self.workYearCode = workYearCode
#         self.compId = compId
#         self.compName = compName
#         self.compTag = compTag
#         self.industry = industry
#         self.salary = salary
#         self.jobKind = jobKind
#         self.compScale = compScale
#         self.compKind = compKind
#         self.compStage = compStage
#         self.eduLevel = eduLevel
#
#     # def create(self):
#     #     db.session.add(self)
#     #     db.session.commit()
#     #     return self
#
#
# class JobRecommendation(db.Model):
#     """建工作推荐表
#
#     Args:
#         Base (_type_): _description_
#     """
#     # 指定映射表名
#     __tablename__ = 'job_recommendation'
#
#     # ID设置为主键
#     id = db.Column(db.Integer, primary_key=True)
#     dataInfo = db.Column(db.String(256))
#     dataParams = db.Column(db.Text)
#     job_title = db.Column(db.String(80))
#     job_salary = db.Column(db.String(20))
#     job_dq = db.Column(db.String(20))
#     job_requireWorkYears = db.Column(db.String(10))
#     job_requireEduLevel = db.Column(db.String(32))
#     job_labels = db.Column(db.String(200))
#     job_link = db.Column(db.String(256))
#
#     jobId = db.Column(db.Integer, unique=True)
#     topJob = db.Column(db.String(10))
#     job_advViewFlag = db.Column(db.String(10))
#     job_dataPromId = db.Column(db.String(100))
#
#     recruiterName = db.Column(db.String(20))
#     recruiterTitle = db.Column(db.String(50))
#
#     recruiter_imId = db.Column(db.String(32))
#     recruiter_imUserType = db.Column(db.String(5))
#     recruiter_chatted = db.Column(db.String(5))
#     recruiterId = db.Column(db.String(32))
#     recruiterPhoto = db.Column(db.String(50))
#
#     compId = db.Column(db.String(20))
#     compName = db.Column(db.String(50))
#     compScale = db.Column(db.String(20))
#     compStage = db.Column(db.String(10))
#     compIndustry = db.Column(db.String(20))
#
#     compLogo = db.Column(db.String(50))
#     comp_link = db.Column(db.String(256))
#
#     job_intro_content = db.Column(db.Text())
#     jobKind = db.Column(db.String(10))
#     job_refreshTime = db.Column(db.String(20))
#     job_origin = db.Column(db.String(10))
#     push_flag = db.Column(db.String(10), default='false')
#
#     username = db.Column(db.String(20))
#     usermail = db.Column(db.String(50))
#
#     utime = db.Column(db.DateTime, server_default=db.func.now())
#     mtime = db.Column(db.DateTime, onupdate=db.func.now())
#
#     __table_args__ = (
#         db.UniqueConstraint('id', 'jobId', name='uix_id_jobId'),
#     )
#
#     def __init__(self, **kwargs):
#         super(JobRecommendation, self).__init__( **kwargs)
#
#
# class jobRequestScheme:  # 二级域名方法
#     def __init__(self) -> None:
#         pass
#
#
# class jobRecommendationScheme:  # 职位推荐方法
#     # def __init__(self, **kwargs) -> None:
#     #     self.kwargs = kwargs
#
#     def insert_job(self, **kwargs):  #
#         try:
#             with Session() as DBSession:
#                 result = DBSession.add(JobRecommendation(**kwargs))
#                 print(f'添加职位 <{kwargs["job_title"]}-{kwargs["job_dq"]}-{kwargs["compName"]}> SUCCESS!')
#         except:
#             print(f'添加职位 <{kwargs["job_title"]}-{kwargs["job_dq"]}-{kwargs["compName"]}> Fail!')
#             print_exc()
#             result = None
#         DBSession.commit()  # 对数据库做了修改
#         return result
#
#     def query_jobId(self, jobId):
#         try:
#             with Session() as DBSession:
#                 result = DBSession.query(JobRecommendation).filter_by(jobId=jobId).one()
#                 print(f'查询到职位 <{jobId}> [{result}]!')
#         except:
#             result = None
#             print(f'未查询到职位 <{jobId}> [{result}]!')
#         return result
#
#     def queryCompNum(self, ):
#         try:
#             with Session() as DBSession:
#                 result = DBSession.query(func.count(JobRecommendation.id)).scalar()
#                 print(f'查询到职位数目 [{result}]!')
#         except Exception as e:
#             result = None
#             print(f'未查询到职位数目 [{result}]!')
#         return result
#
#     def query_distinct_column_count(self, column_name):
#         try:
#             # 使用上下文管理器来管理会话
#             with Session() as DBSession:
#                 # 动态获取列对象
#                 column_obj = getattr(JobRecommendation, column_name)
#
#                 # 查询指定列去重后的数目
#                 distinct_count = DBSession.query(func.count(func.distinct(column_obj))).scalar()
#
#                 print(f'去重后的 {column_name} 数目: {distinct_count}')
#         except Exception as e:
#             # 捕获具体的异常并打印错误信息
#             print(f'查询失败: {e}')
#             distinct_count = None
#         return distinct_count
#
#     def get_top_ten_industries(self):
#         try:
#             # 使用上下文管理器来管理会话
#             with Session() as DBSession:
#                 # 查询 industry 列的值及其出现的次数，并按次数降序排序
#                 result = (
#                     DBSession.query(
#                         JobRecommendation.compIndustry,
#                         func.count(JobRecommendation.compIndustry).label('count')
#                     )
#                     .group_by(JobRecommendation.compIndustry)
#                     .order_by(func.count(JobRecommendation.compIndustry).desc())
#                     .limit(10)  # 取前十个
#                     .all()
#                 )
#
#                 # 将结果转换为所需的格式
#                 formatted_result = [
#                     {'value': count, 'name': compIndustry}
#                     for compIndustry, count in result
#                 ]
#
#                 # 打印结果
#                 for item in formatted_result:
#                     print(item)
#
#                 return formatted_result
#
#         except Exception as e:
#             # 捕获具体的异常并打印错误信息
#             print(f'查询失败: {e}')
#             return []


def is_connected():
    """如果连接到公网则返回True，没有连接到则返回False。"""
    try:
        # 尝试连接到一个公共的 DNS 服务器
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        return True
    except OSError:
        return False


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
            return
    else:  # 离线状态
        return


class LiepinSearchJob:
    """
    猎聘网搜索职位接口
    """
    def __init__(self, payload):
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
            'X-Fscp-Trace-Id': '3650dc5e-2ae9-4a3b-a6f6-b39386dbef4f'  # 'e1929537-67e9-497a-9287-862c1af97549'
        }
        self.mainSearchPcConditionForm = payload
        self.data = {'mainSearchPcConditionForm': '%s' % self.mainSearchPcConditionForm}
        self.form_data = {'data': self.data}

    async def get_job_detail_infos(self, job_link):
        print('【访问】 {job_link}'.format(job_link=job_link))
        async with aiohttp.ClientSession() as session:
            async with session.get(job_link, headers=self.headers, proxy=check_proxy()['http']) as response:
                r = await response
        html = etree.HTML(r.text)
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
        except:
            job_tags = ''

        try:
            job_intro_content = html.xpath('//main//content//dd[@data-selector="job-intro-content"]//text()')[0]
        except IndexError as e:
            job_intro_content = ''
            print('Index Error !!!!!估计被猎聘安全中心发现了!!!!!!quit~~')

        try:
            company_intro = html.xpath(
                '//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')[0]
        except IndexError as e:
            company_intro = html.xpath(
                '//main//content//section[@class="company-intro-container"]//div[@class="inner ellipsis-3"]/text()')
            if (not company_intro):
                company_intro = ''

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
        return job_detail

    async def get_liepin_searchjobs(self):
        currentPage = json.loads(self.mainSearchPcConditionForm)['currentPage'] + 1
        print(f"当前访问第 {currentPage} 页")
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, cookies=self.cookies, json=self.form_data, proxy=check_proxy()['http']) as response:
                return await response.text(), currentPage

    async def process_work(self, **kwargs):
        res_text = kwargs.get('res_text')
        currentPage = kwargs.get('page')
        # print(f'状态码: <{r.status_code}>')
        result_ret = json.loads(res_text)  # r.text
        pagination = result_ret['data']['pagination'] if result_ret['flag'] else []
        totalPage = pagination['totalPage'] if 'totalPage' in pagination else 0

        while currentPage < totalPage:  # totalPage  pageSize
            print(f"当前访问第 {currentPage + 1} 页")
            temp_payload = json.loads(self.mainSearchPcConditionForm)
            temp_payload['currentPage'] += 1
            self.mainSearchPcConditionForm = json.dumps(temp_payload)
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, cookies=self.cookies, json=self.form_data, proxy=check_proxy()['http']) as response:
                    r = await response.text()
            # print(f'状态码: <{r.status_code}>')
            result_next = json.loads(r)
            try:
                result_ret['data']['data']['jobCardList'] += (result_next['data']['data']['jobCardList'] if result_next['flag'] else [])
                pagination = result_next['data']['pagination'] if result_ret['flag'] else []
                currentPage += 1
                totalPage = pagination['totalPage'] if 'totalPage' in pagination else 0
            except Exception as e:
                currentPage += 1
                print(result_ret)
                quit()

        jobCardList = result_ret['data']['data']['jobCardList'] if result_ret['flag'] else []
        print(f'本次职位总计:{len(jobCardList)}')
        # quit()
        jobs = []
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
            # if not self.jobrecommend_oper.query_jobId(jobId=job['jobId']):
            #     self.jobrecommend_oper.insert_job(**jobCnt)
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
        return jobs


async def main():
    # 查询相关职位
    req_data_str = '{"city": "050090", "dq": "050090", "currentPage": 0, "key": "C++开发", "workYearCode": 0}'
    jobFinder = LiepinSearchJob(req_data_str)
    liepin_job_res, currentPage  = await jobFinder.get_liepin_searchjobs()
    # print(liepin_job_res)
    kwargs = {
        "res_text": liepin_job_res,
        "page": currentPage
    }
    # print(kwargs)
    r = await jobFinder.process_work(**kwargs)
    print(r)

    # for _ in liepin_job_res:
    #     # print(_)
    #     job_detail = jobFinder.get_job_detail_infos(_['Job']['job_link'])
    #     # print(job_tags)
    #     # print(job_tags, job_intro)
    #     break

    # 测试二级域名 func
    # sec_op = jobRequestScheme()

    # 测试相关职位数目获取
    # jobrecommend_oper = jobRecommendationScheme()
    # # compNum = jobrecommend_oper.queryCompNum()
    # column_count = jobrecommend_oper.query_distinct_column_count('jobId')
    # column_count = jobrecommend_oper.query_distinct_column_count('compName')
    # column_count = jobrecommend_oper.query_distinct_column_count('compIndustry')
    # column_count = jobrecommend_oper.query_distinct_column_count('job_dq')
    # # print(f'职位数目: {compNum}')
    # # print(f'column数目: {column_count}')

    # 统计liepin最多职位的十个行业
    # top_ten_industries = jobrecommend_oper.get_top_ten_industries()
    # print(top_ten_industries)


if __name__ == '__main__':
    asyncio.run(main())
