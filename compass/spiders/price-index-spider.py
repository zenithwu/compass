# -*- coding: utf-8 -*-
import json
import os
import time

import scrapy
from compass.items import WeatherItem, CompassItem


class PriceIndexSpider(scrapy.Spider):
    name = 'price-index-spider'
    start_urls = [
        'http://www.100ppi.com/cindex/',
    ]
    data_path=os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))

    custom_settings = {
        'ITEM_PIPELINES': {
            'compass.pipelines.JsonLinesExporterPipeline': 1
        }
    }

    def parse(self, response):
        for type_url in response.xpath('//div[@class="band"]//a'):
            url = str(type_url.xpath("@href").extract_first())
            n = str(type_url.xpath("text()").extract_first()).strip()
            # print(response.urljoin(url))
            yield scrapy.Request(url=response.urljoin(url), meta={"name":n},callback=self.parse_price)

    def parse_price(self, response):

        li=response.xpath('//div[@class="left2"]//td/text()').extract()
        n=response.meta['name']
        v=li[len(li)-1]
        yield self.parse_data(n,v)

    def parse_data(self,n,v):
        item = CompassItem()
        item["info"] = {"name":n,"value":v}
        return item


if __name__ == '__main__':
    from scrapy import cmdline

    name = PriceIndexSpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
