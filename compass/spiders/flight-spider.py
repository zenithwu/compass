# -*- coding: utf-8 -*-
import os
import time

import scrapy

from compass.items import PriceItem, FlightItem
from scrapy import Selector


class FlightSpider(scrapy.Spider):
    name = 'flight-spider'
    start_urls = [
        'http://www.variflight.com/sitemap/flight?AE71649A58c77=',
    ]
    data_path = os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))

    custom_settings = {
        'ITEM_PIPELINES': {
            'compass.pipelines.JsonLinesExporterPipeline': 1
        }
    }

    def parse(self, response):
        for info in response.xpath('//div[@class="innerRow"]//a'):
            url=info.xpath("@href").extract_first()
            position=info.xpath("text()").extract_first()
            yield scrapy.Request(url=response.urljoin(url), meta={"position": position},callback=self.parse_list)



    def parse_list(self, response):
        print("---")
        for info in response.xpath('//div[@class="li_com"]'):
            item=FlightItem()
            position=response.meta['position']
            if position is not None and str(position).find('-')>-1:
                item['start']=str(position).split("-")[0]
                item['end']=str(position).split("-")[1]
            item['info']=info.xpath("span[1]//a[1]/text()").extract_first()
            item['no']=info.xpath("span[1]//a[2]/text()").extract_first()
            item['start_time']=info.xpath("span[2]/text()").extract_first().strip()
            item['start_position']=info.xpath("span[4]/text()").extract_first()
            item['end_time']=info.xpath("span[5]/text()").extract_first().strip()
            item['end_position']=info.xpath("span[7]/text()").extract_first()
            item['status']=info.xpath("span[9]/text()").extract_first()
            yield item

if __name__ == '__main__':
    from scrapy import cmdline

    name = FlightSpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
