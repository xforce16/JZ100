# -*- coding: utf-8 -*-
import json
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
        .replace('[]','').replace('<p>','').replace('</p>','')

class ToutiaoNews(scrapy.Spider):
    name = 'toutiao'

    def start_requests(self):
        with open('d:\\test.txt','r',encoding='utf-8') as f:
            keywords = f.readlines()
            for keyword in keywords:
                print(keyword)
                start_urls =  'https://www.toutiao.com/search_content/?offset=0&format=json&keyword={}&autoload=true&count=20&cur_tab=1&from=search_tab'.format(parse.quote(keyword.encode('utf-8')))
                print(start_urls)
                yield scrapy.Request(url = start_urls,callback = self.parse,dont_filter=True,meta = {'company' :keyword})

    def parse(self, response):

        item = NewsItem()
        keyword =response.meta['company']
        # print(response.body)
        js = json.loads(response.body)
        data = js['data']
        # print(data)
        url_list=[]
        for i in data:
            if 'article_url' in i.keys() :
                item['title'] = i['title']
                item['abstract'] = i['abstract']
                item['source'] = i['source']
                item['article_url'] = i['article_url']
                yield scrapy.Request(url=item['article_url'],callback = self.parse_detail,dont_filter=True,meta = {'company' :keyword,
                                                                                                   'item': deepcopy(item)})

    def parse_detail(self,response):
        item = response.meta['item']
        print('*'*100)
        item['company'] = response.meta['company']
        # item['title'] = response.css('::text').extract_first()
        item['content'] = response.xpath("//body//p//text()").extract()
        print(item['content'])
        # item['content'] = "".join(item['content'] )

        # item['content'] = re.findall("^<p>(.*)</p>",item['content'])
        # item['content'] = ListCombiner(response.xpath('./p//text()').extract())
        # item['content'] = "".join(item['content'] )
        # item['content'] = re.findall(r"[\u4e00-\u9fa5]*",item['content'])
        # item['content'] = "".join(item['content'])

        print(item)




