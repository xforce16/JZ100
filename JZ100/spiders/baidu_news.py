# -*- coding: utf-8 -*-
import re
from copy import deepcopy
import scrapy
from JZ100.items import NewsItem
from urllib import parse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import logging


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    logger = logging.getLogger(__name__)

    def start_requests(self):
        with open('d:\\test2.txt','r',encoding='utf-8') as f:
            keywords = f.readlines()
            for keyword in keywords:
                print("开始获取",keyword,"*"*100)
                start_urls = 'http://news.baidu.com/ns?word={}&tn=news&from=news&cl=2&rn=20&ct=1'.format(parse.quote(keyword.encode('gb2312')))
                print(start_urls)
                yield scrapy.Request(url = start_urls,callback = self.parse,dont_filter=True,meta = {'company' :keyword})

    def parse(self, response):
        item =deepcopy(NewsItem())
        item['company'] =response.meta['company']
        news_amount = response.xpath("//span[@class='nums']").extract_first()
        amount = re.search(r'\d+(,\d+)*',news_amount)
        print(amount)
        # 相关新闻数量
        item['amount'] = int(amount.group(0).replace(',',''))
        print (item['amount'])
        if item['amount'] != 0:
            url_list = response.xpath("//div[@class='result']")
            print (url_list)
            if url_list is not None:
                for u in url_list:
                    item['title'] = u.xpath(".//h3/a//text()").extract()
                    item['title'] = "".join(item['title']).strip()
                    item['article_url'] = u.xpath(".//h3/a/@href").extract_first()
                    item['publish_data'] = u.xpath(".//p[@class='c-author']/text()").extract_first()
                    item['publish_data']= re.search(r"(\d){4,}.*(\d)", item['publish_data']).group(0)
                    item['source'] = u.xpath(".//p[@class='c-author']/text()").extract_first()
                    item['source'] = re.search(r"[\u4e00-\u9fa5]*", item['source']).group(0)
                    item['abstract'] = u.xpath(".//div[@class='c-summary c-row ']//text()").extract()[2:-4]
                    item['abstract'] = "".join(item['abstract']).strip()
                    print(item)
                    yield scrapy.Request(item['article_url'], callback = self.pare_detail, dont_filter=False,meta ={'item' : deepcopy(item)})
        else:
            self.logger.warning("没有找到相关新闻")
            print(item)
            yield item

        next_page = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_page is not None:
            keyword = item['company']
            print(next_page)
            next_page = 'http://news.baidu.com' + next_page
            yield scrapy.Request(next_page,callback = self.parse,dont_filter=False,meta={'item': item,
                                                                       'company':keyword})
    def pare_detail(self,response):
        item = response.meta["item"]
        item['content'] =ListCombiner(response.xpath('//p/text()').extract()[:-3])
        print (item)
        yield item


def ListCombiner(lst):
    string = ""
    for e in lst:
        string += e
    return string.replace(' ','').replace('\n','').replace('\t','')\
        .replace('\xa0','').replace('\u3000','').replace('\r','')\
        .replace('[]','')
