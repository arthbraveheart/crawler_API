import scrapy

class ChatubaProduct(scrapy.Item):
  
   
    ean   = scrapy.Field()
    price = scrapy.Field() 
    url   = scrapy.Field()