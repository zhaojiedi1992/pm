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
            "#detail-data tbody tr":{
                '__use': 'dump',  # dump data directly
                '__list': True,  # it's a list
                'name': ':nth-child(1)::text',
                'aqi': ':nth-child(2)::text',
                'level': ':nth-child(3)::text',
                'firstgas': ':nth-child(4)::text',
                'pm25': ':nth-child(5)::text',
                'pm10': ':nth-child(6)::text',
                'co': ':nth-child(7)::text',
                'no2': 't:nth-child(8)::text',
                'o3': ':nth-child(9)::text',
                'o3_h8': ':nth-child(10)::text',
                'so2': ':nth-child(11)::text'
            }
    }
    def parse(self, response):
        for it in response.css("div.all li a::attr(href)").extract():
            yield  response.follow(it,self.parse2)
    def parse2(self, response):
        #info('Parse------------------>> ' + response.url)
        # x = self.parse_with_rules(response, self.list_css_rules, dict)
        #info(response.css(#detail-data tbody tr:nth-child(1)::text))
        #x = self.parse_with_rules(response, self.list_css_rules_for_item, dict)
        y =self.parse_with_rules(response,self.list_css_rules_for_item,PmItem)
        #info(x)
        #info("yyy" *20)
        #info(y)
        return y