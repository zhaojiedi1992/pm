import re
import json
from urllib.parse import urlparse
import urllib
import datetime
#import pdb


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
#from pm.comm.spider import CommonSpider
from pm.items import *
#from pm.comm.log import *


class pmSpider(scrapy.Spider):
    name = "pm"
    #allowed_domains = ["pm25.in"]
    start_urls = [
        "http://www.pm25.in"
    ]
    list_css_rules = {
        'div.all li a': {
            'url': 'a::attr(href)',
            'room_name': 'a::attr(title)',
            'tag': 'span.tag.ellipsis::text',
            'people_count': '.dy-num.fr::text'
        }
    }

    list_css_rules_for_item = {
            ".container":{
                    #'__use': 'dump',  # dump data directly
                    '__list': True,  # it's a list
                    ".avg":{
                        '__use': 'dump',  # dump data directly
                        '__list': True,  # it's a list
                        "city": "h2::text",
                        "monitortime": "div.live_data_time p::text"
                    },
                    "city": "h2::text",
                    "monitortime": "div.live_data_time p::text",
                    "#detail-data tbody tr": {
                        '__use': 'dump',  # dump data directly
                        '__list': True,  # it's a list
                        'positionname': ':nth-child(1)::text',
                        'aqi': ':nth-child(2)::text',
                        'pollutantlevel': ':nth-child(3)::text',
                        'primarypollutant': ':nth-child(4)::text',
                        'pm25': ':nth-child(5)::text',
                        'pm10': ':nth-child(6)::text',
                        'co': ':nth-child(7)::text',
                        'no2': 't:nth-child(8)::text',
                        'o3': ':nth-child(9)::text',
                        'o3_h8': ':nth-child(10)::text',
                        'so2': ':nth-child(11)::text',


                     }
                }
    }
    def parse(self, response):
        for it in response.css("div.all li a::attr(href)").extract():
            yield  response.follow(it,self.parse2)
    def parse2(self, response):
        result=[]
        #info('Parse------------------>> ' + response.url)
        # x = self.parse_with_rules(response, self.list_css_rules, dict)
        #info(response.css(#detail-data tbody tr:nth-child(1)::text))
        #x = self.parse_with_rules(response, self.list_css_rules_for_item, dict)
        cityItem= PmItem()
        cityItem["iscity"]=1
        cityItem["monitortime"]=response.css("div.live_data_time p::text").extract_first("_")
        cityItem["scrapytime"] = datetime.datetime.now()
        cityItem["city"]=response.css("h2::text").extract_first("_")
        cityItem["positionname"]=cityItem["city"]
        tmpValue=response.css("div.value")
        cityItem["aqi"]=tmpValue[0].css("::text").extract_first("_")
        cityItem["pm25"]= tmpValue[1].css("::text").extract_first("_")
        cityItem["pm10"] = tmpValue[2].css("::text").extract_first("_")
        cityItem["co"] = tmpValue[3].css("::text").extract_first("_")
        cityItem["no2"] = tmpValue[4].css("::text").extract_first("_")
        cityItem["o3"] = tmpValue[5].css("::text").extract_first("_")
        cityItem["o3_8h"] = tmpValue[6].css("::text").extract_first("_")
        cityItem["so2"] = tmpValue[7].css("::text").extract_first("_")
        cityItem["pollutantlevel"] = response.css("h4::text").extract_first("_")
        cityItem["primarypollutant"] = response.css(".primary_pollutant p::text").extract_first("_")
        #info(cityItem)
        result.append(cityItem)
        #yield cityItem
        #yield cityItem
        for it in response.css("#detail-data tbody tr"):
        #try :
            td = it.css("td")
            if len(td) == 11:
                subItem=PmItem()
                subItem["iscity"] = 2
                subItem["scrapytime"]=datetime.datetime.now()
                subItem["monitortime"] = response.css("div.live_data_time p::text").extract_first("_")
                subItem["city"] = response.css("h2::text").extract_first("_")
                subItem["positionname"]=td[0].css("::text").extract_first("_")
                subItem["aqi"] = td[1].css("::text").extract_first("_")
                subItem["pm25"] = td[4].css("::text").extract_first("_")
                subItem["pm10"] = td[5].css("::text").extract_first("_")
                subItem["co"] = td[6].css("::text").extract_first("_")
                subItem["no2"] = td[7].css("::text").extract_first("_")
                subItem["o3"] =td[8].css("::text").extract_first("_")
                subItem["o3_8h"] = td[9].css("::text").extract_first("_")
                subItem["so2"] = td[10].css("::text").extract_first("_")
                subItem["pollutantlevel"]=td[2].css("::text").extract_first("_")
                #subItem["primarypollutant"]=td[3].css("::text").extract_first("_")
                subItem["primarypollutant"] = "".join(td[3].css("::text").extract())
                yield subItem
            #result.append(subItem)
        #except:
         #   pass
            #yield  subItem
        #y =self.parse_with_rules(response,self.list_css_rules_for_item,PmItem)
        #info(x)
        #info("yyy" *20)
        #info(result)
        #return result
