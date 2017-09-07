from sqlalchemy import Column, String, create_engine,INTEGER,NUMERIC
from sqlalchemy.dialects.oracle import DATE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy import func,and_
import cx_Oracle
# 创建对象的基类:
Base = declarative_base()
# 定义T_BUS_AIR_QUALITY_HOUR对象:
class T_BUS_AIR_QUALITY_HOUR(Base):
    # 表的名字:
    __tablename__ = 'T_BUS_AIR_QUALITY_HOUR'
    # 表的结构:
    id = Column(INTEGER, primary_key=True)
    #city = Column(String(300))
    #cityid = Column(String(300))
    #positionname = Column(String(300))
    aqi = Column(String(300))
    primarypollutant = Column(String(300))
    so2 = Column(String(300))
    no2 = Column(String(300))
    co = Column(String(300))
    o3 = Column(String(300))
    o3_8h = Column(String(300))
    pm25 = Column(String(300))
    pm10 = Column(String(300))
    monitortime = Column(DATE)
    scrapytime = Column(DATE)
    #stationid = Column(NUMERIC)
    stationcode = Column(String(300))
    pollutantlevel= Column(String(300))
   #lon = Column(NUMERIC)
    #lat = Column(NUMERIC)
class T_BAS_AIR_STATION(Base):
    __tablename__ = 'T_BAS_AIR_STATION'
    id = Column(INTEGER, primary_key=True)
    stationname=Column(String(300))
    city=Column(String(300))
    city_pp = Column(String(300))
    lon = Column(NUMERIC)
    lat = Column(NUMERIC)
    iscity = Column(String(300))
    controllevel = Column(String(300))
    stationcode = Column(String(300))
class databaseTool:
    def __init__(self):
        self.engine = create_engine('oracle+cx_oracle://comm:oracle@59.108.92.221:1521/orcl')
        self.DBSession = sessionmaker(bind=self.engine)
    def start(self):
        self.session = self.DBSession()
        sql="alter session set nls_date_format = 'yyyy-mm-dd hh24:mi:ss'"
        self.session.execute(sql)
    def getStationInfo(self):
        #s=select([T_BAS_AIR_STATION])
        s = select([T_BAS_AIR_STATION.stationcode, T_BAS_AIR_STATION.city,T_BAS_AIR_STATION.stationname])
        result=self.session.execute(s)
        return result
    def addobj(self,hour):
        #newobj = T_BUS_AIR_QUALITY_HOUR(hour)
        stmt=select([func.count(T_BUS_AIR_QUALITY_HOUR.id)]).where(and_( T_BUS_AIR_QUALITY_HOUR.monitortime==hour.monitortime,T_BUS_AIR_QUALITY_HOUR.stationcode==hour.stationcode ))
        tmp =self.session.execute(stmt).fetchall()
        if tmp[0][0]==0:
            self.session.add(hour)
            self.session.commit()
        else:
            pass
    def close(self):
        self.session.close()
if __name__ == "__main__":
    tool= databaseTool()
    tool.start()
    obj={"stationcode": "2634A","monitortime":"2017-08-18 16:00:00"}
    hour = T_BUS_AIR_QUALITY_HOUR(**obj)
    tool.addobj(hour)
    #result= list(tool.getStationInfo())

    #print(result[0])
    #print(result)
    tool.close()
