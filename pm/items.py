# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    iscity = scrapy.Field()
    positionname = scrapy.Field()
    aqi = scrapy.Field()
    pollutantlevel = scrapy.Field()
    primarypollutant = scrapy.Field()
    pm25 = scrapy.Field()
    pm10 = scrapy.Field()
    co = scrapy.Field()
    no2 = scrapy.Field()
    o3 = scrapy.Field()
    o3_8h = scrapy.Field()
    so2 = scrapy.Field()
    # other
    id = scrapy.Field()
    city = scrapy.Field()
    cityid = scrapy.Field()
    monitortime = scrapy.Field()
    scrapytime = scrapy.Field()
    stationid = scrapy.Field()
    stationcode = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()

