# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:58:50 2024

@author: ArthurRodrigues
"""

import scrapy
from chatubascraper.itemloaders import ChatubaProductLoader
from chatubascraper.items import ChatubaProduct 
from pandas import read_pickle 
import re
import json
import urllib
import base64

class ChatubaSpider(scrapy.Spider):

   name       = 'chatubaspider'
   refs       = read_pickle('C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/ChatubaMap.pkl')
   start_urls = ['https://www.chatuba.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=ea653273-ac5e-448e-9cde-0a75024c9ab9&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22fd92698fe375e8e4fa55d26fa62951d979b790fcf1032a6f02926081d199f550%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOmZhbHNlLCJtYXAiOiJjIiwicXVlcnkiOiJwaXNvcy1lLXJldmVzdGltZW50b3MiLCJvcmRlckJ5IjoiT3JkZXJCeVNjb3JlREVTQyIsImZyb20iOjAsInRvIjoyMywic2VsZWN0ZWRGYWNldHMiOlt7ImtleSI6ImMiLCJ2YWx1ZSI6InBpc29zLWUtcmV2ZXN0aW1lbnRvcyJ9XSwiZmFjZXRzQmVoYXZpb3IiOiJTdGF0aWMiLCJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ImRlZmF1bHQiLCJ3aXRoRmFjZXRzIjpmYWxzZSwic2hvd1Nwb25zb3JlZCI6dHJ1ZX0%3D%22%7D']
   
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_generator = getALL(self.start_urls[0], 2759, self.refs)
        self.next_url = next(self.url_generator, None)

   def parse(self, response):
        product = ChatubaProductLoader(item=ChatubaProduct(), selector=response)
        product.add_value('ean', response.text)
        product.add_value('price', response.text)
        product.add_value('url', response.text)
        yield product.load_item()

        if self.next_url:
            next_page_url = self.next_url
            self.next_url = next(self.url_generator, None)
            yield response.follow(next_page_url, callback=self.parse)  


def getProducts(url : str , rng : tuple, ref : str) -> str:
    # Extract the query parameters from the URL
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Extract the 'extensions' parameter
    extensions_encoded = query_params['extensions'][0]

    # URL decode the 'extensions' parameter
    extensions_decoded = urllib.parse.unquote(extensions_encoded)

    # Parse the decoded JSON string
    extensions_obj = json.loads(extensions_decoded)#[:-1] + '"}') #extension string fixed

    # Extract the 'variables' parameter
    variables_encoded = extensions_obj['variables']

    # Base64 decode the 'variables' parameter
    variables_decoded = base64.b64decode(variables_encoded).decode('utf-8')

    # Parse the JSON string to get the original JSON object
    variables_obj = json.loads(variables_decoded)

    # Modify the variables object
    variables_obj['from'] = rng[0]
    variables_obj['to']   = rng[1]
    variables_obj['query']= ref#'material-de-construcao'
    variables_obj['selectedFacets'][0]['value'] = variables_obj['query']
    # Convert the modified object to a JSON string
    modified_variables_json = json.dumps(variables_obj)
    # Base64 encode the JSON string
    modified_variables_encoded = base64.b64encode(modified_variables_json.encode('utf-8')).decode('utf-8')
    # Update the extensions object with the new encoded variables
    extensions_obj['variables'] = modified_variables_encoded
    # Convert the updated extensions object to a JSON string
    updated_extensions_json = json.dumps(extensions_obj)
    # URL encode the JSON string
    updated_extensions_encoded = urllib.parse.quote(updated_extensions_json)

    # Construct the new URL with the updated 'extensions' parameter
    new_query_params = query_params
    new_query_params['extensions'] = updated_extensions_encoded
    # Construct the new URL
    #new_url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(new_query_params, doseq=True)))

    url_base = 'https://www.chatuba.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=ea653273-ac5e-448e-9cde-0a75024c9ab9&operationName=productSearchV3&variables=%7B%7D&extensions='

    new_urlll = url_base + updated_extensions_encoded

    return new_urlll




def getALL(url : str, n : int, refs : list):
     
    i=0
    chunk = 99
    #querys = (ref in refs)
    for ref in refs: 
        while True:
             if i<ref[1]:
                 tup     = (i,i+chunk)
                 new_url = getProducts(url,tup,ref[0])
                 i = i+chunk
                 yield new_url
             else:
                 tup = (i-chunk,ref[1])
                 new_url = getProducts(url,tup,ref[0])
                 yield new_url
                 break

  
