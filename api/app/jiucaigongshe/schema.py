# from config import Config
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# from app.jiucaigongshe.models import BlockInfo
#
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
# Base = declarative_base()  # 建立 sql rom基类
# Session = sessionmaker(bind=engine)
#
#
# class blockSearchScheme:  # 二级域名方法
#     def __init__(self) -> None:
#         pass
#
#     def insertBlocks(self, block_name, info_num):
#         DBSession = Session()
#         # second_domain = '.'.join([third_domain.split('.')[-2], third_domain.split('.')[-1]])
#         # 查询三级域名的ID
#         block_item = DBSession.query(BlockInfo).filter_by(block_name=block_name).one()
#         # second_domain_id = second_domain.id
#         try:
#             result = DBSession.add(BlockInfo(
#                 block_name=block_name,
#                 info_num=info_num,
#             ))
#             # print(f'添加三级域名 <{third_domain}> SUCCESS!')
#         except:
#             DBSession.close()
#             # print(f'添加三级域名 <{third_domain}> Fail!')
#             # print_exc()
#             result = None
#         DBSession.commit()
#         DBSession.close()
#         return result
