from sqlalchemy import Column, String, create_engine,INTEGER,NUMERIC,DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cx_Oracle
# 创建对象的基类:
Base = declarative_base()
# 定义T_BUS_AIR_QUALITY_HOUR对象:
class T_BUS_AIR_QUALITY_HOUR(Base):
    # 表的名字:
    __tablename__ = 'T_BUS_AIR_QUALITY_HOUR'
    # 表的结构:
    id = Column(INTEGER, primary_key=True)
    city = Column(String(300))
    cityid = Column(String(300))
    positionname = Column(String(300))
    aqi = Column(NUMERIC)
    primarypollutant = Column(String(300))
    so2 = Column(NUMERIC)
    no2 = Column(NUMERIC)
    co = Column(NUMERIC)
    o3 = Column(NUMERIC)
    o3_8h = Column(NUMERIC)
    pm25 = Column(NUMERIC)
    pm10 = Column(NUMERIC)
    monitortime = Column(DATETIME)
    scrapytime = Column(DATETIME)
    stationid = Column(NUMERIC)
    stationcode = Column(String(300))
    lon = Column(NUMERIC)
    lat = Column(NUMERIC)
# 初始化数据库连接:
#engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
engine = create_engine('oracle://comm:oracle@59.108.92.221:1521/orcl')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
newobj= T_BUS_AIR_QUALITY_HOUR(id=1)
session.add(newobj)
#session.execute("select * from dba_data_files")
session.commit()
session.close()