import scrapy

class BalaProduct(scrapy.Item):
  
    url = scrapy.Field()
    eans = scrapy.Field()
    price = scrapy.Field()    