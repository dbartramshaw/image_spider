# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
Item Pipeline
After an item has been scraped by a spider, it is sent to the Item Pipeline
which processes it through several components that are executed sequentially.
Each item pipeline component (sometimes referred as just “Item Pipeline”)
is a Python class that implements a simple method.

They receive an item and perform an action over it, also deciding if the item
should continue through the pipeline or be dropped and no longer processed.

Typical uses of item pipelines are:
 - cleansing HTML data
 - validating scraped data (checking that the items contain certain fields)
 - checking for duplicates (and dropping them)
 - storing the scraped item in a database

 """


#
# import json
# class JsonWriterPipeline(object):
#     """The following pipeline stores all scraped items (from all spiders) into a single items.jl file,
#     containing one item per line serialized in JSON format:
#     """
#     def open_spider(self,spider):
#         print('JSON BABY!!!')
#         #print(item.keys())
#         self.file = open('dbs_items.json', 'w')
#
#     def close_spider(self, spider):
#         self.file.close()
#
#     def process_item(self, item, spider):
#         print(item.keys())
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item




import json
class ImgDetailJsonWriterPipeline(object):
    def open_spider(self,spider):
        # Setup json files
        self.file_img = open('full_imgs.json', 'w')
        self.file_desc = open('full_descs.json', 'w')
        self.author = open('authors.json', 'w')

    def close_spider(self, spider):
        self.file_img.close()
        self.file_desc.close()
        self.author.close()

    def process_item(self, item, spider):
        # set image and details save
        if spider.name == 'img-multi-condition-save':
            #print('!!! FIRST ITEM !!!',item.keys()[0])
            if item.keys()[0]=='set_likes':
                line = json.dumps(dict(item)) + "\n"
                self.file_desc.write(line)
                #print('!!! IMG DESC WRITTEN !!!')
            else:
                line = json.dumps(dict(item)) + "\n"
                self.file_img.write(line)
                #print('!!! IMAGE WRITTEN !!!')
            return item

        # Save author urls
        if spider.name == "author-profile-urls":
            line = json.dumps(dict(item)) + "\n"
            self.author.write(line)
            return item





#####################################
# OTHER USEFUL PIPELINES
#####################################
# import pymongo
# class MongoPipeline(object):
#
#     collection_name = 'scrapy_items'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(dict(item))
#         return item


# import scrapy
# import hashlib
# from urllib.parse import quote

# class ScreenshotPipeline(object):
#     """Pipeline that uses Splash to render screenshot of
#     every Scrapy item.
#
#     #login & screenshot example
#     #https://stackoverflow.com/questions/22687235/website-scraping-and-screenshots
#
#
#     """
#
#     SPLASH_URL = "http://localhost:8050/render.png?url={}"
#
#     def process_item(self, item, spider):
#         encoded_item_url = quote(item["url"])
#         screenshot_url = self.SPLASH_URL.format(encoded_item_url)
#         request = scrapy.Request(screenshot_url)
#         dfd = spider.crawler.engine.download(request, spider)
#         dfd.addBoth(self.return_item, item)
#         return dfd
#
#     def return_item(self, response, item):
#         if response.status != 200:
#             # Error happened, return item.
#             return item
#
#         # Save screenshot to file, filename will be hash of url.
#         url = item["img_url"]
#         url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
#         filename = "{}.png".format(url_hash)
#         with open(filename, "wb") as f:
#             f.write(response.body)
#
#         # Store filename in item.
#         item["screenshot_filename"] = filename
#         return item
