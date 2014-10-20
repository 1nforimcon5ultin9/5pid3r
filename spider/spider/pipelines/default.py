# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import os.path
import hashlib
from spider.utils import *
from urlparse import urlparse
class SpiderPipeline(object):
    def __init__(self, settings):
        self.store_uri = settings.get("CONTENT_STORE")
        self.post_uri = settings.get("POST_URL")
        self.settings = settings
        if not os.path.exists(self.store_uri):
            os.makedirs(self.store_uri)
        pass

    def process_item(self, item, spider):
        print '''










































































        fuck











































        '''
        domain = spider.domain
        data = convert_to_json(item["author"],item["url"], item["body"],item["title"],item["crawled_time"], item["crawled_timemills"],self.settings.get("IS_ENCODE"))
        if self.settings.get("ENABLE_POST")==True:
            try:
                post_json(self.post_uri, data)
            except Exception as e:
                spider.log("ERROR: cannot post, please check the post_uri");
        if self.settings.get("PERSIST_TEXT")==True:
            if not item["url"]==None:
                o = urlparse(item["url"])
                base_url=o.netloc
                if ":" in base_url:
                    base_urls = base_url.split(":")
                    if len(base_urls)>0:
                        base_url = base_urls[0]
                    else:
                        base_url=""
                file_path = hashlib.sha1(item["url"]).hexdigest()
                persist_text(self.store_uri,domain+"/"+ base_url+"/"+file_path, data)
        return item

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)





