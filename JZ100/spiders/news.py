# -*- coding: utf-8 -*-
import re
from copy import deepcopy
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
        with open('c:\\test.txt','r',encoding='utf-8') as f:
            keywords = f.readlines()
            for keyword in keywords:
                print(keyword)
                start_urls = 'https://search.sina.com.cn/?q={}&range=all&c=news&sort=time'.format(parse.quote(keyword.encode('gb2312')))
                print(start_urls)
                yield scrapy.Request(url = start_urls,callback = self.parse,dont_filter=True,meta = {'company' :keyword})


    def parse(self, response):
        item =NewsItem()
        item['company'] =response.meta['company']
        news_amount = response.css('.l_v2::text').extract_first()
        amount = re.search(r'\d+(,\d+)*',news_amount)
        # 相关新闻数量
        item['amount'] = int(amount.group(0).replace(',',''))
        print (amount)
        # 相关新闻网址
        url_list = response.css(".result .box-result ")
        print (url_list)
        if url_list is not None:
            for u in url_list:
                item['title'] = u.xpath(".//h2/a/text()").extract()
                item['href'] = u.xpath(".//h2/a/@href").extract_first()
                item['brief'] = u.xpath(".//p//text()").extract()

                # item['brief'] = re.findall("[\u4e00-\u9fa5]",item['brief'])
                item['brief'] = "".join(item['brief'])
                print(item)
                # yield scrapy.Request(item['href'], callback = self.pare_detail, dont_filter=True,meta ={'item' : deepcopy(item)})


        # next_page = response.xpath("//a[text()='下一页']/@href").extract_first()

    def pare_detail(self,response):

        item = response.meta["item"]
        # item['title'] = response.xpath("//h1[@id='artibodyTitle']//text()").extract()
        # item['content'] =ListCombiner(response.xpath('//p/text()').extract()[:-3])
        print (item)






