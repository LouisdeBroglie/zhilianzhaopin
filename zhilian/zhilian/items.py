# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail_url = scrapy.Field()
    detail = scrapy.Field()
    job = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    educational = scrapy.Field()
    experience = scrapy.Field()
    requirement = scrapy.Field()
    work_palce = scrapy.Field()
