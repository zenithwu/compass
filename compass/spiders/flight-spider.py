# -*- coding: utf-8 -*-
import os
import time

import scrapy

from compass.items import PriceItem
from scrapy import Selector


class FlightSpider(scrapy.Spider):
    name = 'flight-spider'
    start_urls = [
        'http://www.variflight.com/flight/fnum/3U3030.html?AE71649A58c77=',
    ]
    data_path = os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))

    custom_settings = {
        'ITEM_PIPELINES': {
            'compass.pipelines.JsonLinesExporterPipeline': 1
        }
    }

    def parse(self, response):
        type_name = ""
        # for type_url in response.xpath('//div[@id="sites"]//dl/*/*'):
        #     n = str(type_url.xpath("text()").extract_first())
        #     if n is not None:
        #         if n.find("频道") > -1:
        #             type_name = n.strip()
        #         else:
        #             url = str(type_url.xpath("@href").extract_first()).strip()
        #             n = n.strip()
        #             n = n[0:len(n) - 1]
        #             # print(response.urljoin(url), n, type_name)
        #             yield scrapy.Request(url=response.urljoin(url), meta={"name": n, "t_name": type_name},
        #                                  callback=self.parse_price)

    def parse_price(self, response):
        if len(response.xpath('//table[@class="lp-table"]/tr').extract()) >= 2:
            item = PriceItem()
            item['t_name'] = response.meta['t_name']
            item['name'] = response.meta['name']
            info = Selector(text=response.xpath('//table[@class="lp-table"]/tr').extract()[1])
            if len(info.xpath('//td').extract()) < 5:
                return
            else:
                if len(info.xpath('//td').extract()) == 5:
                    item['price_type'] = info.xpath('//td[3]/text()').extract_first()
                    item['price'] = info.xpath('//td[4]/text()').extract_first()
                    item['price_reportime'] = info.xpath('//td[5]/text()').extract_first()
                    item['company'] = info.xpath('//td[2]/div/text()').extract_first()
                if len(info.xpath('//td').extract()) == 6:
                    item['price_type'] = info.xpath('//td[2]/text()').extract_first()
                    item['price'] = info.xpath('//td[3]/text()').extract_first()
                    item['price_reportime'] = info.xpath('//td[6]/text()').extract_first()
                    item['company'] = info.xpath('//td[1]//a/text()').extract_first()

                item['price_type'] = item['price_type'].strip() if item['price_type'] is not None else None
                item['price_reportime'] = item['price_reportime'].strip() if item['price_reportime'] is not None else None

                item['company'] = item['company'].strip() if item['company'] is not None else None
                return item


if __name__ == '__main__':
    from scrapy import cmdline

    name = FlightSpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
