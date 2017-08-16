# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    aqi=scrapy.Field()
    level= scrapy.Field()
    firstgas = scrapy.Field()
    pm25 = scrapy.Field()
    pm10 = scrapy.Field()
    co= scrapy.Field()
    no2= scrapy.Field()
    o3 = scrapy.Field()
    o3_h8= scrapy.Field()
    so2=scrapy.Field()
    pass