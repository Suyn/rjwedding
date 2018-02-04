from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'rj'
USERNAME = 'root'
PASSWORD = 'lk1997'

db_url = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    DATABASE
)

engine = create_engine(db_url)

Session = sessionmaker(engine)
session = Session()

Base = declarative_base(engine)