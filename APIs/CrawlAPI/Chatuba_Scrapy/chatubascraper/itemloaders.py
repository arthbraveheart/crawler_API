from itemloaders.processors import TakeFirst, MapCompose, Compose, Identity
from scrapy.loader import ItemLoader
import re



class ChatubaProductLoader(ItemLoader):
    
    default_output_processor = Identity()
            
    def extract_ean(self, dumped_json):

         pattern_ean   = re.compile(r'"Value":"(\d+)"')
         match         = re.findall(pattern_ean, dumped_json)
         if match:
             return match
         return None
    
    def extract_url(self, dumped_json):

         pattern_link  = re.compile(r'"link":"(.*?)"')
         match         = re.findall(pattern_link, dumped_json)
         if match:
             return match
         return None
    
    def extract_price(self, dumped_json):

         pattern_price = re.compile(r'"Price":(\d+\.\d+)')
         match         = re.findall(pattern_price, dumped_json)
         if match:
             return match
         return None
    
    
    ean_in   = MapCompose(lambda x :  ChatubaProductLoader().extract_ean(x) )
    price_in = MapCompose(lambda x: ChatubaProductLoader().extract_price(x))
    url_in   = MapCompose(lambda x : ChatubaProductLoader().extract_url(x) )
    


