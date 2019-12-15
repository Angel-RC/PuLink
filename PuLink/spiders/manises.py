import sys
sys.path.append('C:/Users/Chicote/Desktop/PuLink/PuLink')
from items import manisesItem

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
import datetime
#from PuLink.items import manisesItem
import items

from scrapy.crawler import CrawlerProcess



class spider_manises(CrawlSpider):
    name           = 'spider_manises'
    entidad        = 'Hospital Sanitas'
    ciudad         = 'Valencia'
    url_site       = 'https://www.hospitalmanises.es/'
    allowed_domain = ['https://careers.talentclue.com/es/company/YTozOntzOjQ6InRleHQiO3M6MzI6IhyOtuF7wNavxoyz92pDLWX6wCiQSpRvXOSuy39SaB8pIjtzOjY6Im1ldGhvZCI7czoxNDoibWNyeXB0X3Jpal8yNTYiO3M6ODoia2V5X25hbWUiO3M6MTU6InNlY3VyZV9maWxlX2tleSI7fQ%2C%2C/offers/menu/modal']
    start_urls     = ['https://careers.talentclue.com/es/company/YTozOntzOjQ6InRleHQiO3M6MzI6IhyOtuF7wNavxoyz92pDLWX6wCiQSpRvXOSuy39SaB8pIjtzOjY6Im1ldGhvZCI7czoxNDoibWNyeXB0X3Jpal8yNTYiO3M6ODoia2V5X25hbWUiO3M6MTU6InNlY3VyZV9maWxlX2tleSI7fQ%2C%2C/offers/menu/modal']

    def parse(self, response):

        empleo_list = response.xpath("//table[@id='company-jobs-widget-table']/tbody/tr")

        for empleo_item in empleo_list:

            oferta = manisesItem()

            oferta['start_date']     = empleo_item.xpath("td[5]/text()").get()
            oferta['entidad']        = self.entidad
            oferta['ciudad']         = empleo_item.xpath("td[3]/text()").get()
            oferta['provincia']      = empleo_item.xpath("td[4]/text()").get()
            oferta['titulo']         = empleo_item.xpath("td[1]/a/text()").get().replace("\n", '').replace("\r", '')
            oferta['unidad_negocio'] = empleo_item.xpath("td[2]/text()").get()
            oferta['url']            = empleo_item.xpath("td[1]/a/@href").get()
            oferta['deadline']       = "Sin fecha limite. "
            oferta['referencia']       = " - "

            yield oferta

if __name__ == "__main__":
    process = CrawlerProcess({
        'FEED_URI': 'data/manises.csv',
        'FEED_FORMAT': 'csv'
    })
    process.crawl(spider_manises)
    process.start()
