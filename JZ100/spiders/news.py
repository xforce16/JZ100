# -*- coding: utf-8 -*-
import re

import copy
import scrapy
from JZ100.items import NewsItem
from urllib import parse

def ListCombiner(lst):
    string = ""
    for e in lst:
        string += e
    return string.replace(' ','').replace('\n','').replace('\t','')\
        .replace('\xa0','').replace('\u3000','').replace('\r','')\
        .replace('[]','')

class NewsSpider(scrapy.Spider):
    name = 'news'
    page_num = 1


    def start_requests(self):
        with open('d:\\test.txt','r',encoding='utf-8') as f:
            keywords = f.readlines()
            for keyword in keywords:
                print(keyword)
                start_urls = 'https://search.sina.com.cn/?q={}&range=all&c=news&sort=rel'.format(parse.quote(keyword.encode('gb2312')))
                print(start_urls)
                yield scrapy.Request(url = start_urls,callback = self.parse,dont_filter=True,meta = {'company' :keyword})


    def parse(self, response):
        keyword =response.meta['company']

        news_amount = response.css('.l_v2').xpath("text()").extract_first()
        amount = re.search(r'\d+(,\d+)*',news_amount)
        # 相关新闻数量
        amount = int(amount.group(0).replace(',',''))

        print (amount)
        # 相关新闻网站
        url_list = response.css(".r-info h2 a").xpath("@href").extract()


        company = keyword

        next_page = response.xpath("//a[text()='下一页']/@href").extract_first()
        print (next_page)
        if next_page:
            yield scrapy.Request(url = 'https://search.sina.com.cn' + next_page , callback = self.parse,meta = {'company' :keyword,
                                                                                                                'list':url_list})

        for url in url_list:
             yield scrapy.Request(url = url,callback = self.pare_detail,meta = {'company':company,
                                                                                'amount' :amount
                                                                                })

    def pare_detail(self,response):

        item = NewsItem()
        item['company'] = response.meta['company']
        item['amount'] =response.meta['amount']
        item['title'] = response.xpath("//h1[@id='artibodyTitle']/text()").extract()[0]
        item['content'] =ListCombiner(response.xpath('//p/text()').extract()[:-3])
        print (item)
        # print(url_list)





