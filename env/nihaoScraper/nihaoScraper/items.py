# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class NihaoscraperItem(scrapy.Item):

    category = scrapy.Field(input_processor = MapCompose(remove_tags), output_procesor = TakeFirst())
    subcategory = scrapy.Field(input_processor = MapCompose(remove_tags), output_procesor = TakeFirst())

    product_key = scrapy.Field()
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_procesor = TakeFirst())
    link = scrapy.Field()
    price = scrapy.Field(input_processor = MapCompose(remove_tags), output_procesor = TakeFirst())

    weight = scrapy.Field()
    stock = scrapy.Field()
    subProductName = scrapy.Field()
    subProductPrice = scrapy.Field()