# from traceback import print_exc
#
# from app.liepin.models import JobRecommendation
# from config import Config
# from sqlalchemy import create_engine, func
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
# Base = declarative_base()  # 建立 sql rom基类
# Session = sessionmaker(bind=engine)
#
#
# class jobRequestScheme:  # 二级域名方法
#     def __init__(self) -> None:
#         pass
#
#     # 添加记录
#     # def insert_job(self, username, usermail, city, dq, pubTime, currentPage, \
#     #     pageSize, Key, suggestTag, workYearCode, compId, compName, compTag, \
#     #         industry, salary, jobKind, compScale, compKind, compStage, eduLevel):
#     #     DBSession = Session()
#     #     try:
#     #         result = DBSession.add(JobRequest(
#     #             username='bcy',
#     #             usermail='saintbcy@163.com',
#     #             city='050090',
#     #             dq='050090',
#     #             pubTime='',
#     #             currentPage=0,
#     #             pageSize=40,
#     #             Key='爬虫',
#     #             suggestTag='',
#     #             workYearCode='1$3',
#     #             compId='',
#     #             compName='',
#     #             compTag='',
#     #             industry='',
#     #             salary='10$20',
#     #             jobKind='2',
#     #             compScale='070',
#     #             compKind='',
#     #             compStage='',
#     #             eduLevel='040'
#     #         ))
#     #         print(f'添加二级域名 <{second_domain}> SUCCESS!')
#     #     except:
#     #         DBSession.close()
#     #         print(f'添加二级域名 <{second_domain}> Fail!')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return result
#
#     # # 删除记录
#     # def delete_domain(self, second_domain):
#     #     DBSession = Session()
#     #     try:
#     #         result = DBSession.query(SecondDomain).filter(SecondDomain.second_domain==second_domain).delete()
#     #         print(f'删除二级域名 <{second_domain}> SUCCESS!')
#     #     except:
#     #         DBSession.close()
#     #         print(f'删除二级域名 <{second_domain}> Fail!')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return result
#
#     # # 更新记录
#     # def update_subdomain_num(self, second_domain, sub_domain_num):
#     #     DBSession = Session()
#     #     try:
#     #         rows_changed = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).update(
#     #             dict(sub_domain_num = sub_domain_num)
#     #         )
#     #         if rows_changed:
#     #             print(f'更改二级域名 <{second_domain}> 数量为 [{sub_domain_num}]!')
#     #         else:
#     #             print(f'未发现二级域名 <{second_domain}> !')
#     #     except:
#     #         DBSession.close()
#     #         print(f'更改二级域名 <{second_domain}> 数量 Fail!')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return rows_changed
#
#     # # 查询记录
#     # def query_record(self, second_domain):
#     #     DBSession = Session()
#     #     try:
#     #         result = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).one()
#     #         print(f'查询到二级域名 <{second_domain}> [{result}]!')
#     #     except:
#     #         DBSession.close()
#     #         result = None
#     #         print(f'未查询到二级域名 <{second_domain}> !')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return result
#
#     # def query_three_level_dn_num(self, query_id):
#     #     DBSession = Session()
#     #     try:
#     #         result = DBSession.query(ThirdDomain).filter_by(second_domain_id=query_id).all()
#     #         print(len(result))
#     #         print(f'查询到三级域名数量[{len(result)}]!')
#     #     except:
#     #         DBSession.close()
#     #         result = None
#     #         print(f'未查询到二级域名子域名!')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return len(result)
#
#     # def get_id_by_sec_dname(self, second_domain):
#     #     DBSession = Session()
#     #     try:
#     #         result = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).one()
#     #         result_id = result.id
#     #         print(f'查询到二级域名 <{second_domain}> id:[{result_id}]!')
#     #     except:
#     #         DBSession.close()
#     #         result_id = None
#     #         print(f'未查询到二级域名 <{second_domain}> !')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return result_id
#
#
# class jobRecommendationScheme:  # 职位推荐方法
#     # def __init__(self) -> None:
#     #     pass
#
#     # 添加记录
#     def insert_job(self, **kwargs):  #
#         try:
#             with Session() as DBSession:
#                 result = DBSession.add(JobRecommendation(**kwargs))
#                 print(f'添加职位 <{kwargs["job_title"]}-{kwargs["job_dq"]}-{kwargs["compName"]}> SUCCESS!')
#         except Exception as e:
#             print(f'添加职位 <{kwargs["job_title"]}-{kwargs["job_dq"]}-{kwargs["compName"]}> Fail!')
#             print_exc()
#             result = None
#         DBSession.commit()
#         return result
#
#     # # 删除记录
#     # def delete_domain(self, third_domain):
#     #     DBSession = Session()
#     #     try:
#     #         result = DBSession.query(ThirdDomain).filter(ThirdDomain.third_domain==third_domain).delete()
#     #         print(f'删除三级域名 <{third_domain}> SUCCESS!')
#     #     except:
#     #         DBSession.close()
#     #         print(f'删除三级域名 <{third_domain}> Fail!')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return result
#
#     # # 更新记录
#     # def update_subdomain_num(self, third_domain, sub_domain_num):
#     #     DBSession = Session()
#     #     try:
#     #         rows_changed = DBSession.query(ThirdDomain).filter_by(third_domain=third_domain).update(
#     #             dict(sub_domain_num = sub_domain_num)
#     #         )
#     #         if rows_changed:
#     #             print(f'更改三级域名 <{third_domain}> 数量为 [{sub_domain_num}]!')
#     #         else:
#     #             print(f'未发现三级域名 <{third_domain}> !')
#     #     except:
#     #         DBSession.close()
#     #         print(f'更改三级域名 <{third_domain}> 数量 Fail!')
#     #     DBSession.commit()
#     #     DBSession.close()
#     #     return rows_changed
#
#     # # 查询记录
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
#     def queryJobNum(self, ):
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
#
#
# if __name__ == '__main__':
#     # 清空表
#     # 创建表
#     # Base.metadata.create_all(engine)
#     # result = DBSession.query(SecondDomain).filter_by(second_domain='www.baidu.com').one()
#
#     # 测试二级域名 func
#     sec_op = jobRequestScheme()
#
#     # 测试三级域名 func
#     # sec_op = thirdDomainScheme()
#
#     # TEST
#     # Add
#     # result = sec_op.insert_job(username='bcy',usermail='saintbcy@163.com',city='050090',dq='050090',\
#     #     pubTime='',currentPage=0,pageSize=40,Key='爬虫',suggestTag='',workYearCode='1$3',compId='',\
#     #         compName='',compTag='',industry='',salary='10$20',jobKind='2',compScale='070',compKind='',\
#     #             compStage='',eduLevel='040')
#     # # result = sec_op.insert_domain(third_domain='tieba.baidu.com')
#
#     # # Delete
#     # # result = sec_op.delete_domain(second_domain='google.com')
#     # # Update
#     # # result = sec_op.update_subdomain_num(second_domain='baidu.com', sub_domain_num=1)
#     # # Query
#     # # result = sec_op.query_record(second_domain='baidu.com')
#     # # result = sec_op.query_record(third_domain='tiebabaidu.com')
#     # # result = sec_op.get_id_by_sec_dname(second_domain='baidu.com')
#
#     # # 查询三级域名数量
#     # # result = sec_op.query_three_level_dn_num(query_id=1)
#     # print(result)
