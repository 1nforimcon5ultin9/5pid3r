import os
import os.path
import urllib2
import httplib2
import base64
import json
def _get_filesystem_path(store_uri,key):
    path_comps = key.split('/')
    return os.path.join(store_uri, *path_comps)

def persist_text(store_uri, path, text):
    absolute_path = _get_filesystem_path(store_uri,path)         
    dirname=os.path.dirname(absolute_path);
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(absolute_path, "wb") as f:
        f.write(text)

def tika_parse_text(buf,server_url,content_type=None):
    req = urllib2.Request(server_url, data=buf)
    req.get_method = lambda: 'PUT'
    if not content_type == None:
        req.add_header('Content-Type', content_type)
    res = urllib2.urlopen(req)
    return res.read()

def convert_to_json(author,url, doc, title, time, timemills, update_time, is_encode=False):
    data={}
    if not url==None:
        data["url"]=url
    if not author==None:
        data["author"]=author
    if not title==None:
        data["title"] = title
    if not time==None:
        data["crawled_time"] = time
    if not timemills==None:
        data["crawled_timemills"]=timemills
    if not doc==None:
        data["doc"]=filter(lambda x:x not in ["\n","\t","\r"],doc)
    if not update_time==None:
        data["update_time"] = update_time
    if is_encode==True:
        data["doc"]=base64.b64encode(data["doc"])
    return json.dumps(dict(data),ensure_ascii=False).encode("utf-8")

def post_json(url,json):
    h = httplib2.Http()
    resp, con = h.request(url, 'POST', json, headers={'Content-Type':'application/json'})
#tika_parse_text("asdfasdf", "http://localhost:8999/tika")

