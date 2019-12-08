# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class PulinkItem(scrapy.Item):
    # define the fields for your item here like:
    start_date = scrapy.Field()
    entidad = scrapy.Field()
    ciudad = scrapy.Field()
    titulo = scrapy.Field()
    deadline = scrapy.Field()
    referencia = scrapy.Field()
    url = scrapy.Field()

