import sys
#sys.path.append('C:/Users/Chicote/Desktop/proyectos/Pulink/PuLink')
#from items import PulinkItem

class PulinkItem(scrapy.Item):
    # define the fields for your item here like:
    start_date = scrapy.Field()
    entidad = scrapy.Field()
    ciudad = scrapy.Field()
    titulo = scrapy.Field()
    deadline = scrapy.Field()
    referencia = scrapy.Field()
    url = scrapy.Field()

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
import datetime


class spider_fisabio(CrawlSpider):
    name           = 'spider_fisabio'
    entidad        = 'FISABIO'
    ciudad         = 'Valencia'
    url_site       = 'http://fisabio.san.gva.es/'
    allowed_domain = ['http://fisabio.san.gva.es/empleo']
    start_urls     = ['http://fisabio.san.gva.es/empleo']
    N_PAGES        = 3 # no habra empleo en mas de 3 paginas, no merece la pena mirar el resto

    def parse(self, response):
        page_list = [self.url_site + "empleo?startelem=" + str(i) for i in range(self.N_PAGES)]
        for page_item in page_list:
            yield scrapy.Request(page_item, callback = self.parse_page)

    def parse_page(self, response):
        """
                Parsing of each page.
        """
        empleo_list = response.xpath("//div[@class='portlet-body']/table[4]/tr")
        empleo_list = [
            empleo_item
            for empleo_item in empleo_list
            if datetime.datetime.strptime(empleo_item.xpath("td//tr/td[7]/text()").get(),'%d/%m/%Y').date() > datetime.date.today()
        ]

        for empleo_item in empleo_list:

            oferta = PulinkItem()

            oferta['start_date'] = " - "
            oferta['entidad']    = self.entidad
            oferta['ciudad']     = empleo_item.xpath("td//tr/td[9]/text()").get()
            oferta['titulo']     = empleo_item.xpath("td//tr/td[5]/a/text()").get().replace("\n", '').replace("\r", '')
            oferta['referencia'] = empleo_item.xpath("td//tr/td[3]/text()").get()
            oferta['url']        = empleo_item.xpath("td//tr/td[5]/a/@href").get()
            oferta['deadline']   = empleo_item.xpath("td//tr/td[7]/text()").get()

            yield oferta

if __name__ == "__main__":
    process = CrawlerProcess({
        'FEED_URI': 'data/fisabio.csv',
        'FEED_FORMAT': 'csv'
    })
    process.crawl(spider_fisabio)
    process.start()
