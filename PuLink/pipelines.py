# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals

class ItemPipeline(object):
    def process_item(self, item, spider):
        return item
from scrapy import signals
import os
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exporters import JsonItemExporter

