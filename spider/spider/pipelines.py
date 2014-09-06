# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import os.path
import hashlib
import spider.utils

class SpiderPipeline(object):
    def __init__(self, settings):
        self.store_uri = settings.get("CONTENT_STORE")
        self.post_uri = settings.get("POST_URL")
        self.settings = settings
        if not os.path.exists(self.store_uri):
            os.makedirs(store_uri)
        pass

    def process_item(self, item, spider):
        data = convert_to_json(item["url"], item["body"], self.settings.get("IS_ENCODE"))
        if self.settings.get("ENABLE_POST")==True:
            post_json(self.post_uri, data)
        if self.settings.get("PERSIST_TEXT")==True:
            if not item["url"]==None:
                file_path = hashlib.sha1(item["url"]).hexdigest()
                persist_text(self.store_uri, file_path, data)
        return item

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)





