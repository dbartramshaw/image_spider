# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


#Imgs Demo
class ImageItem(scrapy.Item):

    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


class ImageInfo(scrapy.Item):
    # ... other item fields ...
    image_desc = scrapy.Field()
    image_url = scrapy.Field()
    image_paths = scrapy.Field()
    set_likes = scrapy.Field()
    meta_views = scrapy.Field()
    group_url = scrapy.Field()


class AuthorItem(scrapy.Item):
    set_url = scrapy.Field()
    author_url = scrapy.Field()
