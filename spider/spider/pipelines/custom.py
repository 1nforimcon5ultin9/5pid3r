import os
from cStringIO import StringIO
import hashlib
from scrapy.utils.misc import md5sum
from spider.pipelines.files import FilesPipeline
from spider.utils import *
from urlparse import urlparse
class CustomFilesPipeline(FilesPipeline):
    def file_downloaded(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        content_type= response.headers.get('content-type', None).lower()
        if "bin;" in content_type:
            content_disposition =  response.headers.get("Content-Disposition")
            if not content_disposition == None:
                index = content_disposition.index("filename=")
                filename = content_disposition[(index+len("filename=\"")):len(content_disposition)-1]
                if "." in filename:
                    ext = os.path.splitext(filename)[1]
                    path = path+ext
                    content_type=self.settings.get("FILE_RAW_TYPE").get(ext[1:])
        ret = tika_parse_text(response.body, self.settings.get("TIKA_SERVER"),content_type if not content_type=="bin;" else None)
        data = convert_to_json("", response.url, ret, "", self.settings.get("IS_ENCODE"))
        base_url = ""
        if not request.url==None:
            o = urlparse(request.url)
            base_url=o.netloc
        domain = info.spider.domain
        if self.settings.get("ENABLE_POST"):
            post_url = self.settings.get("POST_URL")
            post_json(post_url, data)
        if self.settings.get("PERSIST_FILE"):
            buf = StringIO(response.body)
            self.store.persist_file(domain+"/"+base_url+"/"+path, buf, info)
        if self.settings.get("PERSIST_TEXT")==True:
            file_path = hashlib.sha1(response.url).hexdigest()
            persist_text( self.text_store_uri,domain+"/"+base_url+"/"+file_path, data)
        checksum = md5sum(buf)
        return checksum

    def __init__(self,settings, download_func=None):
        self.file_store_uri = settings.get('FILES_STORE')
        self.text_store_uri = settings.get('CONTENT_STORE')
        if not os.path.exists(self.text_store_uri):
            os.makedirs(self.text_store_uri)
        pass
        self.settings = settings
        self.store = self._get_store(self.file_store_uri)
        super(FilesPipeline, self).__init__(download_func=download_func)
        self.counter=0

    @classmethod
    def from_settings(cls, settings):
        cls.FILES_URLS_FIELD = settings.get('FILES_URLS_FIELD', cls.DEFAULT_FILES_URLS_FIELD)
        cls.FILES_RESULT_FIELD = settings.get('FILES_RESULT_FIELD', cls.DEFAULT_FILES_RESULT_FIELD)
        cls.EXPIRES = settings.getint('FILES_EXPIRES', 90)
        return cls(settings)
