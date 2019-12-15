import sys
sys.path.append('C:/Users/Chicote/Desktop/PuLink/PuLink')
from items import PulinkItem

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
import datetime


class spider_la_fe(CrawlSpider):
    name           = 'spider_la_fe'
    entidad        = 'La Fe'
    ciudad         = 'Valencia'
    url_site       = 'https://www.iislafe.es'
    allowed_domain = ['https://www.iislafe.es/es/empleo/']
    start_urls     = ['https://www.iislafe.es/es/empleo/']
    N_PAGES        = 5 # no habra empleo en mas de 5 paginas, no merece la pena mirar el resto

    def parse(self, response):
        page_list = response.xpath("//ul[@class='pagination']//a/@href").getall()[: self.N_PAGES]
        for page_item in page_list:
            yield scrapy.Request(self.url_site + page_item, callback = self.parse_page)

    def parse_page(self, response):
        """
                Parsing of each page.
        """
        empleo_list = response.xpath("//div[@class='empleo-item']")
        empleo_list = [empleo for empleo in empleo_list if empleo.xpath("span[@class='status status--open']/text()").get() is not None]

        for empleo_item in empleo_list:

            oferta = PulinkItem()

            oferta['start_date'] = empleo_item.xpath("time/text()").get()
            oferta['entidad']    = self.entidad
            oferta['ciudad']     = self.ciudad
            oferta['titulo']     = empleo_item.xpath("h2/a/text()").get().replace("\n", '').replace("\r", '')
            oferta['referencia'] = empleo_item.xpath("dl/dd[1]/text()").get()
            oferta['url']        = self.url_site + empleo_item.xpath("h2/a/@href").get()
            oferta['deadline']   = empleo_item.xpath("dl/dd[3]/text()").get()

            yield oferta

if __name__ == "__main__":
    process = CrawlerProcess({
        'FEED_URI': 'data/la_fe.csv',
        'FEED_FORMAT': 'csv'
    })
    process.crawl(spider_la_fe)
    process.start()
