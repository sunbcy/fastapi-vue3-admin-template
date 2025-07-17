# from app import db
#
#
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
#     id = db.Column(db.Integer, primary_key=True)  # autoincrement=True, index=True, nullable=False, unique=True, default=18
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
#         pageSize, Key, suggestTag, workYearCode, compId, compName, compTag, \
#             industry, salary, jobKind, compScale, compKind, compStage, eduLevel):
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
#     # def __init__(self, dataInfo, dataParams, job_title, job_salary, job_dq, job_requireWorkYears, \
#     #     job_requireEduLevel, job_labels, job_link, jobId, topJob, job_advViewFlag, job_dataPromId, \
#     #         recruiterName, recruiterTitle, recruiter_imId, recruiter_imUserType, recruiter_chatted, \
#     #             recruiterId, recruiterPhoto, compId, compName, compScale, compStage, compIndustry, \
#     #                 compLogo, comp_link, job_intro_content, jobKind, job_refreshTime, job_origin, \
#     #                      username, usermail, push_flag='false'):
#     #     self.dataInfo = dataInfo
#     #     self.dataParams = dataParams
#     #     self.job_title = job_title
#     #     self.job_salary = job_salary
#     #     self.job_dq = job_dq
#     #     self.job_requireWorkYears = job_requireWorkYears
#     #     self.job_requireEduLevel = job_requireEduLevel
#     #     self.job_labels = job_labels
#     #     self.job_link = job_link
#     #     self.jobId = jobId
#     #     self.topJob = topJob
#     #     self.job_advViewFlag = job_advViewFlag
#     #     self.job_dataPromId = job_dataPromId
#     #     self.recruiterName = recruiterName
#     #     self.recruiterTitle = recruiterTitle
#     #     self.recruiter_imId = recruiter_imId
#     #     self.recruiter_imUserType = recruiter_imUserType
#     #     self.recruiter_chatted = recruiter_chatted
#     #     self.recruiterId = recruiterId
#     #     self.recruiterPhoto = recruiterPhoto
#     #     self.compId = compId
#     #     self.compName = compName
#     #     self.compScale = compScale
#     #     self.compStage = compStage
#     #     self.compIndustry = compIndustry
#     #     self.compLogo = compLogo
#     #     self.comp_link = comp_link
#     #     self.job_intro_content = job_intro_content
#     #     self.jobKind = jobKind
#     #     self.job_refreshTime = job_refreshTime
#     #     self.job_origin = job_origin
#     #     self.push_flag = push_flag
#     #     self.username = username
#     #     self.usermail = usermail
#     #     # self.utime = utime
#     #     # self.mtime = mtime
#
#     # def create(self):
#     #     db.session.add(self)
#     #     db.session.commit()
#     #     return self
#
