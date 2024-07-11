import scrapy

class SGeraldoProduct(scrapy.Item):
  
    url = scrapy.Field()
    eans = scrapy.Field()
    price = scrapy.Field()    