# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import csv
import codecs
from collections import OrderedDict
#from pm.comm.log import *
from pm.items import PmItem
from pm.spiders.pmData import *
class PmPipeline(object):
    def process_item(self, item, spider):
        return item
def trimsignal(str):
    return str.replace("\n","").replace(" ","")
def changeOneData(item):
    it = item
    it["monitortime"]=it["monitortime"].replace(u"数据更新时间：", "")
    if it["iscity"] == 2:
        it["primarypollutant"] = trimsignal(it["primarypollutant"])
        pass
    elif it["iscity"] == 1:
        it["aqi"] = trimsignal(it["aqi"])
        it["pm25"] = trimsignal(it["pm25"])
        it["pm10"] = trimsignal(it["pm10"])
        it["co"] = trimsignal(it["co"])
        it["pm25"] = trimsignal(it["aqi"])
        it["no2"] = trimsignal(it["no2"])
        it["o3"] = trimsignal(it["o3"])
        it["o3_8h"] = trimsignal(it["o3_8h"])
        it["so2"] = trimsignal(it["so2"])
        it["pollutantlevel"] = re.findall(r".*（(.+?)）.*", it["pollutantlevel"])[0]
        it["primarypollutant"] = trimsignal(it["primarypollutant"]).replace("首要污染物：", "")
class JsonWithEncodingPipeline(object):
    def __init__(self):
        #info("."*300)
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')
        self.file.write("[\n")
        self.isfirst=True

    def process_item(self, item, spider):
        changeOneData(item)
        if self.isfirst:
            line =json.dumps(dict(item), ensure_ascii=False, sort_keys=False)
            self.isfirst=False
        else:
            line = ",\n" +json.dumps( dict(item), ensure_ascii=False, sort_keys=False)
        self.file.write(line)
        return item
    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

class CsvPipeline(object):
    def open_spider(self, spider):
        self.file = open(r'data_utf8.csv', 'w', encoding='utf-8')
        fieldnames = list(PmItem.fields.keys())
        #self.writer = csv.DictWriter(self.file, fieldnames=fieldnames, dialect='excel')
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()
    def process_item(self, item, spider):
        changeOneData(item)
        if not item.get("city", None) is None:
            self.writer.writerow(dict(item))
<<<<<<< HEAD

class OraclePipeline(object):
    def open_spider(self, spider):
        self.tool = databaseTool()
        self.tool.start()
        self.info=list(self.tool.getStationInfo())
        self.file = open(r'data_utf8.log', 'w', encoding='utf-8')
    def close_spider(self, spider):
        self.tool.close()

    def process_item(self, item, spider):
        changeOneData(item)
        hour = T_BUS_AIR_QUALITY_HOUR()
        #hour = T_BUS_AIR_QUALITY_HOUR(**item)
        keys=list(PmItem.fields.keys())
        for key in keys:
            try:
                setattr(hour,key,item[key])
            except:
                pass
        code = [ it  for it in self.info if it[1]==item["city"] and it[2]==item["positionname"]]
        if len(code) >0:
            setattr(hour, "stationcode",code[0][0] )
        else:
            self.file.write(item["city"]+"," +item["positionname"] +"\n")
        self.tool.addobj(hour)
=======
            return item
>>>>>>> 4f91f40a29983efdc691d5cfcaf3592745ff8f6c
