import re
import json
from urllib.parse import urlparse
import urllib
import pdb


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from pm.comm.spider import CommonSpider
from pm.items import *
from pm.comm.log import *


class pmSpider(CommonSpider):
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
        cityItem["city"]=response.css("h2::text").extract_first()
        cityItem["positionname"]=cityItem["city"]
        cityItem["aqi"]=response.css("div.value::text").extract()[0]
        cityItem["pm25"]= response.css("div.value::text").extract()[1]
        cityItem["pm10"] = response.css("div.value::text").extract()[2]
        cityItem["co"] = response.css("div.value::text").extract()[3]
        cityItem["no2"] = response.css("div.value::text").extract()[4]
        cityItem["o3"] = response.css("div.value::text").extract()[5]
        cityItem["o3_8h"] = response.css("div.value::text").extract()[6]
        cityItem["so2"] = response.css("div.value::text").extract()[7]
        cityItem["pollutantlevel"] = response.css("h4::text").extract_first()
        cityItem["primarypollutant"] = response.css(".primary_pollutant p::text").extract_first()
        info(cityItem)
        result.append(cityItem)
        yield cityItem
        #yield cityItem
        for it in response.css("#detail-data tbody tr"):
            try :
                tmp = it.css("td::text").extract()
                subItem=PmItem()
                subItem["iscity"] = 2
                subItem["city"] = response.css("h2::text").extract_first()
                subItem["positionname"]=tmp[0]
                subItem["aqi"] = tmp[1]
                subItem["pm25"] = tmp[4]
                subItem["pm10"] = tmp[5]
                subItem["co"] = tmp[6]
                subItem["no2"] = tmp[7]
                subItem["o3"] =tmp[8]
                subItem["o3_8h"] = tmp[9]
                subItem["so2"] = tmp[10]
                subItem["pollutantlevel"]=tmp[2]
                subItem["primarypollutant"]=tmp[3]
                info(subItem)
                yield subItem
                result.append(subItem)
            except:
                pass
            #yield  subItem
        #y =self.parse_with_rules(response,self.list_css_rules_for_item,PmItem)
        #info(x)
        #info("yyy" *20)
        info(result)
        #return result
