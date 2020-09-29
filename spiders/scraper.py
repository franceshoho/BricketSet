import scrapy
from ..items import BricksetItem #.. means parent folder

class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    page_number = 2
    # allowed_domains = ['brickset.com']
    # start_urls = [
    #     'https://brickset.com/sets/year-2020/page-1'
    # ]
    # above code is a short cut for all following:
    # def start_requests(self):
    #     start_urls = [
    #         'https://brickset.com/sets/year-2020/page-1'
    #
    #     for url in start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = BricksetItem()
        set_selector = '.set'
        sets = response.css(set_selector)
        # first find the set section and then extract ind. data
        for set in sets:
            name_selector = 'h1 a::text'
            name = set.css(name_selector).extract_first()
            model_selector = 'h1 a span::text'
            model = set.css(model_selector).extract_first()
            model = model.replace(':', "")   # to clean up :
            pieces_selector = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            pieces = set.xpath(pieces_selector).extract_first()
            minifigs_selector = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            minifigs = set.xpath(minifigs_selector).extract_first()
            price_selector = './/dl[dt/text() = "RRP"]/dd[3]/text()'
            price = sets.xpath(price_selector).extract_first()
            usd_price = self.clean_prices(price)

            image_selector = 'img ::attr(src)'
            image = set.css(image_selector).extract_first()

            items['name'] = name
            items['model'] = model
            items['pieces'] = pieces
            items['minifigs'] = minifigs
            items['price'] = usd_price
            items['image'] = image

            yield items

            # USE PAGINATION to follow links
            # You can use this if pages have a structure or
            # you want to limit # of pages scraped to say 10
            next_page = f'https://brickset.com/sets/year-2020/page-{ScraperSpider.page_number}/'
            if ScraperSpider.page_number <= 10:
                ScraperSpider.page_number +=1
                yield response.follow(next_page, callback=self.parse)


    def clean_prices(self, price):
        prices = price.split(',')
        usd_price = prices[0].replace('$', "")
        eur_price = prices[1].replace(' | ',"")
        return usd_price


