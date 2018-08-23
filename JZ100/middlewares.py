# -*- coding: utf-8 -*-


from scrapy import signals
import logging
import random
import time
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message



class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth

    def process_response(self,request,response,spider):
        # print(request.headers)
        return response

#每次请求使用不同user-agent
class UseragentMiddleware(object):

    def process_request(self,request,spider):
        ua = random.choice(spider.settings.get("USER_AGENTS"))
        request.headers["User-Agent"] = ua

    def process_response(self,request,response,spider):
        print(request.headers["User-Agent"])
        return response

#错误处理中心件
class MyRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)


    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)

            time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response


    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):

            time.sleep(random.randint(3, 5))
            self.logger.warning('连接异常, 进行重试...')

            return self._retry(request, exception, spider)