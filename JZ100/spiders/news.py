# -*- coding: utf-8 -*-
import re
from copy import deepcopy
import scrapy
from JZ100.items import NewsItem
from urllib import parse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


def ListCombiner(lst):
    string = ""
    for e in lst:
        string += e
    return string.replace(' ','').replace('\n','').replace('\t','')\
        .replace('\xa0','').replace('\u3000','').replace('\r','')\
        .replace('[]','')

class NewsSpider(scrapy.Spider):
    name = 'news'


    def start_requests(self):
        with open('c:\\test.txt','r',encoding='utf-8') as f:
            keywords = f.readlines()
            for keyword in keywords:
                print(keyword)
                start_urls = 'https://search.sina.com.cn/?q={}&range=all&c=news&sort=time'.format(parse.quote(keyword.encode('gb2312')))
                print(start_urls)
                yield scrapy.Request(url = start_urls,callback = self.parse,dont_filter=True,meta = {'company' :keyword})

    def parse(self, response):
        item =deepcopy(NewsItem())
        item['company'] =response.meta['company']
        news_amount = response.css('.l_v2::text').extract_first()
        amount = re.search(r'\d+(,\d+)*',news_amount)         # 相关新闻数量
        item['amount'] = int(amount.group(0).replace(',',''))
        print (item['amount'])
        if item['amount'] != 0:
            url_list = response.css(".result .box-result ") # 相关新闻网址
            # print (url_list)
            if url_list is not None:
                for u in url_list:
                    item['title'] = u.xpath(".//h2/a//text()").extract()
                    item['title'] = "".join(item['title'])
                    item['article_url'] = u.xpath(".//h2/a/@href").extract_first()
                    item['publish_data'] = u.xpath(".//h2/span/text()").extract_first()
                    item['publish_data']= re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", item['publish_data']).group(0)
                    item['source'] = u.xpath(".//h2/span/text()").extract_first()
                    item['source'] =re.search(r"[\u4e00-\u9fa5]*",item['source']).group(0)
                    item['abstract'] = u.xpath(".//p//text()").extract()
                    item['abstract'] = "".join(item['abstract'])
                    print(item)
                    yield scrapy.Request(item['article_url'], callback = self.pare_detail, dont_filter=True,meta ={'item' : deepcopy(item)})
        else:
            print('没有找到相关新闻')
            print(item)
            # yield item

        next_page = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_page is not None:
            keyword = item['company']
            print(next_page)
            next_page = 'https://search.sina.com.cn/' + next_page
            yield scrapy.Request(next_page,callback = self.parse,meta={'item': item,
                                                                       'company':keyword})

    def pare_detail(self,response):
        item = response.meta["item"]
        # item['content'] =ListCombiner(response.css('#artibody').xpath('//p/text()').extract()[:-3])
        print (item)
        yield item







