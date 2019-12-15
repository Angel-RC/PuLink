import sys
sys.path.append('C:/Users/Chicote/Desktop/PuLink/PuLink')
from items import PulinkItem

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#from PuLink.items import PulinkItem
import datetime
from scrapy.crawler import CrawlerProcess


class spider_incliva(CrawlSpider):
    name           = 'spider_incliva'
    entidad        = 'INCLIVA'
    ciudad         = 'Valencia'
    url_site       = 'https://www.incliva.es/'
    allowed_domain = ['https://www.incliva.es/empleo']
    start_urls     = ['https://www.incliva.es/empleo']
    estado_abierto = ["Abierta", "ABIERTA", "Open", "OPEN"]

    def parse(self, response):
        """
                Parsing of each page.
        """
        # seleccionamos solo los empleos que estan abiertos
        empleo_list = response.xpath("//table[@id='tabla_empleo']/tbody/tr")
        empleo_list = [item for item in empleo_list if item.xpath("td[5]/text()").get() in self.estado_abierto]

        for empleo_item in empleo_list:

            oferta = PulinkItem()

            oferta['start_date'] = empleo_item.xpath("td[3]/text()").get()
            oferta['entidad']    = self.entidad
            oferta['ciudad']     = self.ciudad
            oferta['titulo']     = empleo_item.xpath("td[1]/text()").get().replace("\n", '').replace("\r", '')
            oferta['referencia'] = empleo_item.xpath("td[2]/text()").get()
            oferta['url']        = self.url_site + empleo_item.xpath("td[6]/a/@href").get()
            oferta['deadline']   = empleo_item.xpath("td[4]/text()").get()

            yield oferta

if __name__ == "__main__":
    process = CrawlerProcess({
        'FEED_URI': 'data/incliva.csv',
        'FEED_FORMAT': 'csv'
    })
    process.crawl(spider_incliva)
    process.start()
