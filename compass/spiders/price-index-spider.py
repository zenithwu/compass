# -*- coding: utf-8 -*-
import os
import time

import scrapy

from compass.items import CompassItem


class PriceIndexSpider(scrapy.Spider):
    name = 'price-index-spider'
    start_urls = [
        'http://www.100ppi.com/cindex/',
    ]
    data_path = os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))

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
            yield scrapy.Request(url=response.urljoin(url), meta={"name": n}, callback=self.parse_price)

    def parse_price(self, response):
        v = response.xpath('//div[@class="left2"]//tr[2]/td[last()]/text()').extract_first()
        item = CompassItem()
        item["info"] = {"name": response.meta['name'], "value": v}
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    name = PriceIndexSpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
