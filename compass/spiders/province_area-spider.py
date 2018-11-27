# -*- coding: utf-8 -*-
import os
import time

import scrapy

from compass.items import AreaItem


class ProvinceCitySpider(scrapy.Spider):
    name = 'province_area_spider'
    start_urls = [
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'compass.pipelines.JsonLinesExporterPipeline': 1
        }
    }
    data_path = os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))

    def parse(self, response):
        for type_url in response.xpath('//tr[@class="provincetr"]/td/a'):
            url = type_url.xpath("@href").extract_first()
            province = type_url.xpath("text()").extract_first()
            yield scrapy.Request(url=response.urljoin(url)
                                 , meta={"p_id": str(url).split('.')[0] + "0000", "p_name": province}
                                 , callback=self.parse_city)

    def parse_city(self, response):
        p_id = response.meta['p_id']
        p_name = response.meta['p_name']
        for type_url in response.xpath('//tr[@class="citytr"]'):
            url = type_url.xpath("td/a/@href").extract_first()
            c_id = type_url.xpath("td/a/text()").extract()[0][0:6]
            c_name = type_url.xpath("td/a/text()").extract()[1]

            yield scrapy.Request(url=response.urljoin(url)
                                 , meta={"p_id": p_id, "p_name": p_name, "c_id": c_id, "c_name": c_name}
                                 , callback=self.parse_area)

    def parse_area(self, response):
        p_id = response.meta['p_id']
        p_name = response.meta['p_name']
        c_id = response.meta['c_id']
        c_name = response.meta['c_name']
        for type_url in response.xpath('//tr[@class="countytr"]'):
            # 市辖区
            if len(type_url.xpath("td/a").extract()) == 0:
                a_id = type_url.xpath("td/text()").extract()[0][0:6]
                a_name = type_url.xpath("td/text()").extract()[1]
            else:
                a_id = type_url.xpath("td/a/text()").extract()[0][0:6]
                a_name = type_url.xpath("td/a/text()").extract()[1]
            yield self.parse_data(p_id,p_name,a_id,a_name,c_id,c_name)

    def parse_data(self, p_id,p_name,a_id,a_name,c_id,c_name):
        item = AreaItem()
        item['id'] = a_id
        item['name'] = a_name
        item['city_id'] = c_id
        item['city_name'] = c_name
        item['province_id'] = p_id
        item['province_name'] = p_name
        return item


if __name__ == '__main__':
    from scrapy import cmdline

    name = ProvinceCitySpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
