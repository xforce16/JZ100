# -*- coding: utf-8 -*-

# Scrapy settings for JZ100 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'JZ100'

SPIDER_MODULES = ['JZ100.spiders']
NEWSPIDER_MODULE = 'JZ100.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'JZ100 (+http://www.yourdomain.com)'
USER_AGENTS = 'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50','Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50','Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = "WARNING"
LOG_FILE ='./EROR.LOG'

MONGO_URI='localhost'
MONGO_DB ='NEWS'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN",
    "Connection": "keep-alive",
    # "Cookie": "UOR=,finance.sina.com.cn,; ULV=1534845786251:1:1:1::; SINAGLOBAL=172.16.92.25_1534845786.467970; Apache=172.16.92.25_1534845786.467973; U_TRS1=000000a0.21c37a97.5b7be35a.2ed7630a; U_TRS2=000000a0.21cc7a97.5b7be35a.36e8f01d; lxlrttp=1532434326; hqEtagMode=0; WEB2_OTHER=f236fc0a92d2ce55e95e423abbb7978c; SSCSum=4",
    # "DNT": "1",
    # "Host": "search.sina.com.cn",
    # "Referer": "https://search.sina.com.cn/?t=news",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.1.6000",
    "X-DevTools-Emulate-Network-Conditions-Client-Id": "dcf30bce-afd2-4781-a4e2-c0d985ee5007",
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'JZ100.middlewares.Jz100SpiderMiddleware': 543,
#}


# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'JZ100.middlewares.Jz100DownloaderMiddleware': 543,
   #  'JZ100.middlewares.ProxyMiddleware': 543,
    'JZ100.middlewares.UseragentMiddleware': 544,
    'JZ100.middlewares.MyRetryMiddleware': 500,
    # 'JZ100.middlewares.LocalRetryMiddleware' : 500
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'JZ100.pipelines.Jz100Pipeline': 300,
    'JZ100.pipelines.MongoPipeline': 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
RETRY_ENABLED = True
RETRY_TIMES = 3
# RETRY_HTTP_CODES= [500, 503, 504, 400, 408]
RETRY_PRIORITY_ADJUST = - 1
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]
