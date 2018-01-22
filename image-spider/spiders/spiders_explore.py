import scrapy
from image_spider.items import ImageItem,ImageInfo,AuthorItem

import json
import pandas as pd
import binascii
import pickle
import time
from time import gmtime, strftime
import binascii
import numpy as np
save_path = '/project/'




class QuotesSpider(scrapy.Spider):
    name = "quotes-tutorial"
    """ This is the original tutorial with a few added notes and experiments
    --------------
    USEFUL LINKS
    --------------
    #https://doc.scrapy.org/en/latest/intro/tutorial.html#following-links
    #https://doc.scrapy.org/en/latest/topics/selectors.html#topics-selectors
    #http://zvon.org/comp/r/tut-XPath_1.html
    """
    def start_requests(self):
        #urls=pd.read_csv('test_list.csv',index_col=None)
        #urls=urls[urls.columns[0]].tolist()[0:1]
        urls=['http://all-that-is-interesting.com/david-bowie-photos']
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #Save file manually
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        #initial item from items.py (Where data will be stored)
        item = MyItem()
        img_url = response.css('img').xpath('@src').extract_first()
        print('IMG URL',img_url)

        # Different Ways of accessing data from response
        #print('IMG',response.css('img').extract())
        #print('IMG SRC',response.css('img').xpath('@src').extract())
        #print('IMG NAME CONTAINS IMAGE',response.xpath('//a[contains(@href, "image")]/@href').extract())

        #Loop round each img
        for img in response.css('img'):
            print("IMG LOOP",img.xpath('@src').extract())

        #Original loop - get quotes
        for quote in response.css('div.quote'):
            print( quote.css('span.text::text').extract_first())
            print(response.url)
            print('------------------------------------------------------------------------------------------------------------')
            #get the page title
            print('TITLE: ',response.css('title::text').extract())
            print('TITLE: ',response.xpath('//title/text()').extract_first())
            # Get all divs with calss "quote"
            print('DIV CLASS: ',response.css("div.quote").extract_first())
            #print('IMG',response.css('img').extract())




import urlparse
class img(scrapy.Spider):
    name = "img-simple-1"
    def start_requests(self):
        """ Save first image on page """
        urls=['http://all-that-is-interesting.com/david-bowie-photos']
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        print('FILENAME',filename)
        item = ImageItem()
        img_url = response.css('img').xpath('@src').extract_first()
        print('!!! NEW !!!',img_url)
        yield scrapy.Request(img_url,callback=self.parseSingleImage,  meta={'item': item})

    def parseSingleImage(self, response):
        img_url = response.url
        print('YIELDED',img_url)
        yield ImageItem(image_urls=[img_url])




class img_multi(scrapy.Spider):
    name = "img-multi"
    def start_requests(self):
        urls=['http://all-that-is-interesting.com/david-bowie-photos']
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('URL',response.url)
        #loop through all images on page
        for sel in response.css('img'):
            item = ImageItem()
            img_url = sel.xpath('@src').extract_first()
            yield scrapy.Request(img_url,callback=self.parseImages,  meta={'item': item})

    def parseImages(self, response):
        print("!!! RESPONSE TEST !!!", response,response.url)
        img_url = response.url
        yield ImageItem(image_urls=[img_url])





class img_multi_condition(scrapy.Spider):
    name = "img-multi-condition"
    def start_requests(self):
        save_path = '/project/'
        set_id_resultsBIG = pickle.load( open(save_path+"set_id_results.pickle", "rb" ))
        #remove ones that have already been ran
        urls = list(set(set_id_resultsBIG)-set(complete_grps))
        # urls=['https://www.polyvore.com/romwe/set?id=230015155']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print('URL',response.url)
        #loop through all images on page with condition
        #print('DIV CLASS: ',response.css("img.img_size_m").extract_first())
        likes = response.css(".fav_count::text").extract_first()
        meta_ = response.css(".meta").extract_first()
        url_ = response.url
        for sel in response.css("img.img_size_m"):
            item = ImageItem()
            img_url = sel.xpath('@src').extract_first()
            img_desc = sel.xpath('@alt').extract_first()
            #print('----------------URL',img_url)
            #print('----------------DESC',img_desc)
            yield scrapy.Request(img_url,callback=self.parseImages,  meta={'item': item})
            yield ImageInfo(image_desc=img_desc, image_url=img_url, set_likes=likes, meta_views=meta_ ,group_url=url_)

    def parseImages(self, response):
        #print("!!! RESPONSE TEST !!!", response,response.url)
        img_url = str(response.url)
        print(img_url)
        print([img_url])
        yield ImageItem(image_urls=[img_url])





class img_multi_condition_save(scrapy.Spider):
    name = "img-multi-condition-save"
    def start_requests(self):
        save_path = '/project/'
        set_id_resultsBIG = pickle.load( open(save_path+"set_id_results.pickle", "rb" ))
        #urls=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print('URL',response.url)
        #loop through all images on page with condition
        #print('DIV CLASS: ',response.css("img.img_size_m").extract_first())
        with open(save_path+'scrapy_html/'+binascii.hexlify(response.url)+'.html', 'wb') as f:
            f.write(response.body)
        likes = response.css(".fav_count::text").extract_first()
        meta_ = response.css(".meta").extract_first()
        url_ = response.url
        for sel in response.css("img.img_size_m"):
            item = ImageItem()
            img_url = sel.xpath('@src').extract_first()
            img_desc = sel.xpath('@alt').extract_first()
            #print('----------------URL',img_url)
            #print('----------------DESC',img_desc)
            yield scrapy.Request(img_url,callback=self.parseImages,  meta={'item': item})
            yield ImageInfo(image_desc=img_desc, image_url=img_url, set_likes=likes, meta_views=meta_ ,group_url=url_)

    def parseImages(self, response):
        #print("!!! RESPONSE TEST !!!", response,response.url)
        img_url = str(response.url)
        print(img_url)
        print([img_url])
        yield ImageItem(image_urls=[img_url])




from scrapy.selector import Selector
class author_profile_save(scrapy.Spider):
    name = "author-profile-urls"
    def start_requests(self):
        save_path = '/project/'
        set_id_resultsBIG = pickle.load( open(save_path+"set_id_results.pickle", "rb" ))
        urls = list(set(set_id_resultsBIG))
        #urls=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        group_url = response.url
        author_link = response.css(".createdby").extract_first()
        Link = response.css('.createdby a::attr(href)').extract_first()
        print('LINK:'+Link)
        item = AuthorItem()
        yield AuthorItem(set_url=group_url, author_url=Link )
