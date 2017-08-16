# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
from collections import OrderedDict
import cx_Oracle
from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy.schema import *
from pm.comm.log import *

class PmPipeline(object):
    def process_item(self, item, spider):
        return item
class JsonWithEncodingPipeline(object):
    def __init__(self):
        info("."*300)
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=False) + "\n"
        #line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False, indent=1) + "\n"
        self.file.write(line)
        return item
    def close_spider(self, spider):
        self.file.close()