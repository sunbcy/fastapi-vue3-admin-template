# from app import db
#
#
# class BlockInfo(db.Model):
#     """建板块行情查询表
#
#     Args:
#         Base (_type_): _description_
#     """
#     # 指定映射表名
#     __tablename__ = 'block_info'
#
#     # ID设置为主键
#     id = db.Column(db.Integer, primary_key=True)  # autoincrement=True, index=True, nullable=False, unique=True, default=18
#     block_name = db.Column(db.String(10), unique=True, nullable=False)
#     info_num = db.Column(db.Integer)
