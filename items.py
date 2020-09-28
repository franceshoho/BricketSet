# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BricksetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    pieces = scrapy.Field()
    minifigs = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()

