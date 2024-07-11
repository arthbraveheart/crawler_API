# Scrapy settings for chocolatescraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sgeraldoscraper'

SPIDER_MODULES = ['sgeraldoscraper.spiders']
NEWSPIDER_MODULE = 'sgeraldoscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chocolatescraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# To Storing in AWS S3 Bucket
AWS_ACCESS_KEY_ID = 'myaccesskeyhere'
AWS_SECRET_ACCESS_KEY = 'mysecretkeyhere'



# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   
     'sgeraldoscraper.pipelines.SavingSGeraldo': 500,


}


