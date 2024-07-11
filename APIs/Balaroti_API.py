# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:34:26 2024

@author: ArthurRodrigues

The following code uses the GraphQL API from Balaroti to get info from products


"""

from io import StringIO
import pandas as pd
import requests 
import urllib.parse
import psycopg2
import base64
import json
import re
# The URL you provided
URL = 'https://www.balaroti.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=3d10c899-3307-422f-9440-1b8075245ef3&operationName=productSearchV3&variables=%7B%7D&extensions=%7B"persistedQuery"%3A%7B"version"%3A1%2C"sha256Hash"%3A"fd92698fe375e8e4fa55d26fa62951d979b790fcf1032a6f02926081d199f550"%2C"sender"%3A"vtex.store-resources%400.x"%2C"provider"%3A"vtex.search-graphql%400.x"%7D%2C"variables"%3A"eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOmZhbHNlLCJtYXAiOiJjIiwicXVlcnkiOiJwaXNvcy1lLXJldmVzdGltZW50b3MiLCJvcmRlckJ5IjoiT3JkZXJCeVNjb3JlREVTQyIsImZyb20iOjAsInRvIjoxMSwic2VsZWN0ZWRGYWNldHMiOlt7ImtleSI6ImMiLCJ2YWx1ZSI6InBpc29zLWUtcmV2ZXN0aW1lbnRvcyJ9XSwiZmFjZXRzQmVoYXZpb3IiOiJTdGF0aWMiLCJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ImRlZmF1bHQiLCJ3aXRoRmFjZXRzIjpmYWxzZSwic2hvd1Nwb25zb3JlZCI6dHJ1ZX0%3D%22%7D'

def getProducts(url : str , rng : tuple) -> str:
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
    variables_obj['query']= 'material-de-construcao'
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
    new_url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(new_query_params, doseq=True)))
    
    new_urll = """https://www.balaroti.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=3d10c899-3307-422f-9440-1b8075245ef3&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%20%7B%22version%22%3A%201%2C%20%22sha256Hash%22%3A%20%22fd92698fe375e8e4fa55d26fa62951d979b790fcf1032a6f02926081d199f550%22%2C%20%22sender%22%3A%20%22vtex.store-resources%400.x%22%2C%20%22provider%22%3A%20%22vtex.search-graphql%400.x%22%7D%2C%20%22variables%22%3A%20%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6IGZhbHNlLCAic2t1c0ZpbHRlciI6ICJGSVJTVF9BVkFJTEFCTEUiLCAic2ltdWxhdGlvbkJlaGF2aW9yIjogImRlZmF1bHQiLCAiaW5zdGFsbG1lbnRDcml0ZXJpYSI6ICJNQVhfV0lUSE9VVF9JTlRFUkVTVCIsICJwcm9kdWN0T3JpZ2luVnRleCI6IGZhbHNlLCAibWFwIjogImMiLCAicXVlcnkiOiAicGlzb3MtZS1yZXZlc3RpbWVudG9zIiwgIm9yZGVyQnkiOiAiT3JkZXJCeVNjb3JlREVTQyIsICJmcm9tIjogMCwgInRvIjogNTAsICJzZWxlY3RlZEZhY2V0cyI6IFt7ImtleSI6ICJjIiwgInZhbHVlIjogInBpc29zLWUtcmV2ZXN0aW1lbnRvcyJ9XSwgImZhY2V0c0JlaGF2aW9yIjogIlN0YXRpYyIsICJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ICJkZWZhdWx0IiwgIndpdGhGYWNldHMiOiBmYWxzZSwgInNob3dTcG9uc29yZWQiOiB0cnVlfQ%3D%3D%22%7D"""
    
    url_base = 'https://www.balaroti.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=3d10c899-3307-422f-9440-1b8075245ef3&operationName=productSearchV3&variables=%7B%7D&extensions='

    new_urlll = url_base + updated_extensions_encoded
    
    return new_urlll


class DB:

    """
    def __init__(self):
        self.create_connection()
    """    

    def create_connection(self):
        conn = psycopg2.connect(
            host="localhost",
            database="scrapys",
            user="postgres",
            password="123456")
        return conn    


    def process_item(self, item, spider):
        self.store_in_db(item)
        #we need to return the item below as scrapy expects us to!
        return item

    def store_in_db(self, item):
        conn = self.create_connection()
        curr = conn.cursor()
        curr.execute("""INSERT INTO public."balaroti" (jsons) VALUES (%s);""", (item,))
        conn.commit()


def getALL(url : str, n : int):
    
    i=0
    while True:
        if i<n:
            tup     = (i,i+99)
            new_url = getProducts(url,tup)
            
            #Get new response of the modified url
            response = requests.get(new_url)
            jsons = response.json()
            
            DB().store_in_db(response.text)
            i = i+99
        else:
            tup = (i-99,n)
            new_url = getProducts(url,tup)
            
            #Get new response of the modified url
            response = requests.get(new_url)
            jsons = response.json()
            
            DB().store_in_db(response.text)
            break
            
        
def getJson(url : str, n : int) -> dict:
    
    i=0
    tup     = (i,n)
    new_url = getProducts(url,tup)
    
    #Get new response of the modified url
    response = requests.get(new_url)
    jsons    = response.json()
    
    #DB().store_in_db(jsons)
    return jsons    
        
def parseJson(dumped_json : str) -> dict:
    """
    A ideia é transformar isso num ItemLoader do Scrapy.

    Parameters
    ----------
    dumped_json : str
        É o response.text que vem em formato json.

    Returns
    -------
    dict
        apenas para fins de test, essa saída é um dicionário contendo o que será inserido no banco de dados.

    """
   
    pattern_ean   = re.compile(r'"ean":\s"(\d+)"')
    pattern_price = re.compile(r'"Price":\s+(\d+\.\d+)')
    pattern_link  = re.compile(r'"link":\s+"(.*?)"')
    
    out_put       ={
        'eans': re.findall(pattern_ean, dumped_json),
        'prices': re.findall(pattern_price, dumped_json),
        'links': re.findall(pattern_link, dumped_json),
        }
    return out_put
        
#Get new response of the modified url

#new = getProducts(URL, (0,50))
#response = requests.get(new_urlll)

#jsons = response.json()







