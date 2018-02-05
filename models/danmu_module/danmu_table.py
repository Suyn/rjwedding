from libs.China_time.beijing_time import beijing_time
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from libs.db.connect import Base, session


class Danmu(Base):
    __tablename__ = 'danmu'
    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(25), nullable=False, unique=False)

    creattime = Column(DateTime, default=beijing_time)

    contents = Column(Text, nullable=False)

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def get_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_all_personal(cls, username):
        return session.query(cls).filter_by(username=username).all()


# class Retuser(Base):
#     __tablename__ = 'retuser'
#     r_id = Column(Integer, primary_key=True, autoincrement=True)
#     last_login = Column(DateTime, default=datetime.now)
#     login_num = Column(Integer, default=0)
#     u_id = Column(Integer, ForeignKey('user.id'))

