import scrapy
import json
import os

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
            'http://quotes.toscrape.com/page/3/',
            'http://quotes.toscrape.com/page/4/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        quotes_dict={}
        text=' '

        for quote in response.css('div.quote'):
            #print( quote.css('span.text::text').extract_first())
            #print(response.url)
            #print('------------------------------------------------------------------------------------------------------------')
            #quotes_dict[response.url]=quote.css('span.text::text').extract_first()
            text=text+quote.css('span.text::text').extract_first()
        print response.body
        quotes_dict[response.url]=text

        #CREATE JSON
        if not os.path.isfile('output_test2.json'):
            print('NEW FILE CREATED---------------------------')
            with open('output_test2.json', 'w') as f:
                json.dump(quotes_dict, f)
        #UPDATE JSON
        else:
            print('FILE UPDATED---------------------------')
            with open('output_test2.json') as f:
                data = json.load(f)
            data.update(quotes_dict)
            with open('output_test2.json', 'w') as f:
                json.dump(data, f)




    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').extract_first(),
    #             'author': quote.css('span small::text').extract_first(),
    #             'tags': quote.css('div.tags a.tag::text').extract(),
    #         }
