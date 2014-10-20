# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SpiderItem(Item):
    # define the fields for your item here like:
    # name = Field()
    author=Field()
    url = Field()
    body = Field()
    meta_key = Field()
    meta_description=Field()
    title = Field()
    file_urls=Field()
    files = Field()
    crawled_time=Field()
    crawled_timemills=Field()
    id = Field()
    pass
