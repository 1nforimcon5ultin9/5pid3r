import os
import re
import sys
import time
import urllib2
import lxml.html
import lxml.etree
import uuid
import socket
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy.utils.url import urljoin_rfc
from scrapy import log
from scrapy.exceptions import CloseSpider
from spider.items import SpiderItem
from scrapy.utils.response import get_base_url
from spider.rule.ban import BANURL,BANTOKEN

reload(sys)
sys.setdefaultencoding( "utf-8" )
socket.setdefaulttimeout (5)
WEB_REGEX=r'^(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$'

class DefaultSpider(BaseSpider):
        name="default"

        def __init__(self, name=None, url="", domain="", author="inforimconsulting.com", **kwargs):
            LOG_FILE= "./log/"+domain+"/scrapy_%s.log" % time.strftime('%Y_%m_%d_%H_%M_%s',time.localtime(time.time()))
            dirname = os.path.dirname(LOG_FILE);
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            log.log.defaultObserver = log.log.DefaultObserver()
            log.log.defaultObserver.start()
            log.started = False
            log.start(LOG_FILE)
            super(BaseSpider, self).__init__(name, **kwargs)
            print "start crawling "+ url+ " at domain " + domain
            self.allowed_domains = [domain]
            self.start_urls = [url]
            #self.allowed_domains = ["zjcourt.cn"]
            #self.start_urls = ["http://zx.fuzhou.gov.cn/wstd/fzws/201202/P020120202381684079493.rtf"]
            #self.start_urls = ["http://app.zjcourt.cn//message/article/MsgDownServlet?article_id=20130723000014"]
            #self.start_urls = ["http://www.zjcourt.cn/webfiles/web/file/2013/03/20130328155034585.doc"]
            #self.start_urls = ["http://www.zjcourt.cn/webfiles/web/file/20072012sbdfl.pdf"]
            #self.start_urls = ["http://www.zjcourt.cn/webfiles/web/file/2013/09/20130902103434549.ppt"]
            #self.start_urls = ["http://www.zjcourt.cn/webfiles/web/file/2014/01/20140124164537363.xls"]
            self.domain = domain
            self.close_down = False
            self.r = re.compile(WEB_REGEX)
            self.counter=0
            self.author = author;

        def parse(self, response):
            if hasattr(self, "close_down") and self.close_down:
                raise CloseSpider(self)
            content_type= response.headers.get('content-type', None).lower()
            raw_type = self.settings.get("FILE_RAW_TYPE")
            i = SpiderItem()
            if not "html" in content_type:
                i["url"] = response.url
                i["body"]=""
                i["file_urls"] = [response.url]
                i["author"] = self.author
                i["title"] = ""
            else:
                i = self.parse_content(response)
                links = self.parse_link(response) 
                if links!=None and len(links)!=0:
                    for link in links:
                        if not self.filter_link(link.url):
                            continue
                        log.msg("start crawling new url : "+link.url, level=log.INFO)
                        yield Request(link.url.strip(), self.parse)
            yield i

        def parse_content(self, response):
            i = SpiderItem()
            _uuid = str(uuid.uuid1())
            hxs = HtmlXPathSelector(response)
            meta_key = ""
            meta_description = ""
            title = hxs.select("//head/title/text()").extract()
            body = ""
            root = lxml.html.fromstring(response.body)
            lxml.etree.strip_elements(root, lxml.etree.Comment, "script","style","head","canvas","embed","object")
            body = lxml.html.tostring(root, pretty_print=True,method="text", encoding='utf-8')
            i["body"]=body
            if len(title)>0:
                i["title"]= title[0]
            else:
                i["title"] = ""

            if self.author==None:
                i["author"]=""
            else:
                i["author"] = self.author
            i["meta_key"] = meta_key
            i["meta_description"] = meta_description
            i["id"] = _uuid    
            i["url"]= response.url
            i["file_urls"]=set()
            base_url = get_base_url(response)
            hyperlinks = hxs.select("//a[@href]");
            for h in hyperlinks:
                urls = h.select("@href").extract()
                if urls ==None or len(urls)==0:
                    continue
                url = h.select("@href").extract()[0]
                if url==None or url=="":
                    continue
                for key in self.settings.get("FILE_RAW_TYPE"):
                    if url.endswith("."+key):
                        url = self.relative_to_absolute_url(str(url),base_url)
                        i["file_urls"].add(url)
            i["file_urls"]=list(i["file_urls"])
            return i

        def parse_link(self,response):
            """Basic link parser, extract all the link"""
            link_extractor = SgmlLinkExtractor()
            links = link_extractor.extract_links(response)
            return links 

        def is_url(self,url):
            if self.r.match(url):
                return True
            else:
                return False

        def test_url(self,url):
            resp = urllib2.urlopen(url,timeout=5)
            if resp.getcode() != 200:
                log.msg("url test failure : "+url,level=log.WARNING)
                return False    
            else:
                return True

        def relative_to_absolute_url(self,url,base_url):
            if self.is_url(url):
                return url
            else:
                url= str(urljoin_rfc(base_url, url))
                self.test_url(url)
                return url

        def filter_link(self,link):
            for token in BANTOKEN:
                if token in link:
                    log.msg("ignore url: "+link);
                    return False
            if link in BANURL:
                return False
            return True