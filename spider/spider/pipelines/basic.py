# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import os.path
import json
import hashlib
import httplib2
import base64
class SpiderPipeline(object):
    def __init__(self, store_uri, post_uri):
        self.store_uri = store_uri
        self.post_uri = post_uri
        if not os.path.exists(store_uri):
            os.makedirs(store_uri)
        pass

    def process_item(self, item, spider):
        data = {}
        data["doc"] = filter(lambda x:x not in ["\n","\t","\r"],item["body"])
        data["doc"]=base64.b64encode(data["doc"])
        data["url"] = item["url"]
        jsondata = json.dumps(dict(data),ensure_ascii=False).encode("utf-8")
        file_path = hashlib.sha1(data["url"]).hexdigest()
        self._persist_text(file_path, jsondata)
        h = httplib2.Http()
        if not self.post_uri ==None:
            resp, con = h.request(POST_URL, 'POST', jsondata, headers={'Content-Type':'application/json'})
        return item

    @classmethod
    def from_settings(cls, settings):
        store_uri = settings.get("CONTENT_STORE")
        post_uri = settings.get("POST_URL")
        return cls(store_uri, post_uri)

    def _persist_text(self,path, text):
        absolute_path = self._get_filesystem_path(path)         
        with open(absolute_path, "wb") as f:
            f.write(text)


    def _get_filesystem_path(self, key):
        path_comps = key.split('/')
        return os.path.join(self.store_uri, *path_comps)
