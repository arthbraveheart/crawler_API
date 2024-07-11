from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
#from sgeraldoscraper.spiders import casamattosJSspider as cm
import requests
import pandas as pd

## Storing to DB
#import mysql.connector ## MySQL
import psycopg2 ## Postgres


        
class SavingChatuba(object):

    def __init__(self):
        self.create_connection()
        

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
        for e,p,u in zip(item["ean"],item["price"],item["url"]):
            curr.execute("""INSERT INTO public."chatuba" ("ean", "price", "url") VALUES (%s,%s,%s);""", ( #, urlAPI, jsons) VALUES (%s, %s, %s);""", (
                e,#item["eans"],#[0],
                p,#item["price"],#[0],
                u,#item["url"],#[0]
            ))
            conn.commit()  
        
        
        
