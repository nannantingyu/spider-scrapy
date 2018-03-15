# -*- coding: utf-8 -*-
import scrapy, datetime

class CrawlCryptomisoSpider(scrapy.Spider):
    name = 'crawl_cryptomiso'
    allowed_domains = ['cryptomiso.com']
    start_urls = ['http://cryptomiso.com/']

    custom_settings = {
        'LOG_FILE': 'logs/cryptomiso_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def parse(self, response):
        cryptomisos = response.xpath(".//div[@class='card mt-4']//h4[@class='card-title']")
        for cryptomiso in cryptomisos:
            name = cryptomiso.xpath("./text()").extract_first()
            (rank, name) = name.strip()[0:-2].split(". ")
            commit = cryptomiso.xpath(".//small[@class='float-right']/a/span/text()").extract_first()

            commit = commit[0:-8].replace(",", "")
            commit = 1 if not commit else commit

            yield {
                "name": name,
                "rank": rank,
                "commit": commit
            }
