# Scrapy settings for spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

CACHE_STATUS_ENABLED = True
CACHE_DOWNLOAD_ENABLED = True
CONTENT_STORE="./crawed_pages"
WEBSERVICE_ENABLED=False
LOG_FILE="./log/scrapy.log"

#SCHEDULER = "spider.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = False
#SCHEDULER_QUEUE_CLASS = 'spider.scrapy_redis.queue.SpiderPriorityQueue'

ITEM_PIPELINES = [
'spider.pipelines.default.SpiderPipeline',
    'spider.pipelines.custom.CustomFilesPipeline',
    
    
]
FILES_STORE = './downloads'
FILE_RAW_TYPE={
    "doc":"application/msword",
   # "ppt":"application/vnd.ms-powerpoint",
   # "xls":"application/vnd.ms-excel",
    "rtf":"application/rtf"
}
#Tika Jaxrs Server URL
TIKA_SERVER='http://localhost:9998/tika'
#if persist crawled text locally
PERSIST_TEXT=True
#if persist crawled file locally
PERSIST_FILE=True
#Solr URL
POST_URL="http://localhost:9998/tika"
#if post data to solr
ENABLE_POST=True
#if base64encode data
IS_ENCODE=False

#REDIS_HOST = 'localhost'
#REDIS_PORT = 6379