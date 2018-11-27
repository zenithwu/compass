# -*- coding: utf-8 -*-
import os
import time

import scrapy
from compass.items import WeatherItem


class WeatherSpider(scrapy.Spider):
    name = 'weather-spider'
    start_urls = [
        'https://www.tianqi.com/chinacity.html',
    ]
    data_path=os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))
    custom_settings = {
        'ITEM_PIPELINES': {
            'compass.pipelines.JsonLinesExporterPipeline': 1
        }
    }
    pro_dict = dict()

    def parse(self, response):

        # province
        for p_index, provine in enumerate(response.xpath('//div[@class="citybox"]/h2/a')):
            p_name = provine.xpath('text()').extract_first()
            p_url = provine.xpath('@href').extract_first()
            self.pro_dict[p_index] = p_name
            yield scrapy.Request(url=response.urljoin(p_url),
                                 meta={"index": p_index, "province": p_name, "city": p_name, "area": None}
                                 , callback=self.parse_weather)

        # city
        city_val = ""
        for c_index, city_g in enumerate(response.xpath('//div[@class="citybox"]/span')):

            # 市级省的区解析
            if len(city_g.xpath('h3')) == 0:
                for city in city_g.xpath('a'):
                    c_name = city.xpath('text()').extract_first()
                    url = city.xpath('@href').extract_first()
                    yield scrapy.Request(url=response.urljoin(url),
                                         meta={"index": c_index, "province": self.pro_dict[c_index], "city": c_name,
                                               "area": None}
                                         , callback=self.parse_weather)
            else:
                # 普通省份的市县解析
                for city in city_g.xpath('*'):
                    # city
                    if len(city.xpath('a')) > 0:
                        c_name = city.xpath('a/text()').extract_first()
                        a_name = None
                        url = city.xpath('a/@href').extract_first()
                        city_val = c_name
                    else:
                        # area
                        c_name = city_val
                        a_name = city.xpath('text()').extract_first()
                        url = city.xpath('@href').extract_first()
                    yield scrapy.Request(url=response.urljoin(url),
                                         meta={"index": c_index, "province": self.pro_dict[c_index], "city": c_name,
                                               "area": a_name}
                                         , callback=self.parse_weather)

    def parse_weather(self, response):
        weather_info = response.xpath('//dl[@class="weather_info"]')
        show_name = weather_info.xpath('dd[@class="name"]/h2/text()').extract_first()
        # 删除掉非市级省的记录即根据省名称没有天气信息
        if show_name is None:
            return
        item = WeatherItem()
        item['index'] = response.meta['index']
        item['province'] = response.meta['province']
        item['city'] = response.meta['city']
        item['area'] = response.meta['area']

        item['name'] = show_name
        item['temperature'] = weather_info.xpath('dd[@class="weather"]/span/text()').extract_first()
        item['weather'] = weather_info.xpath('dd[@class="weather"]/span/b/text()').extract_first()
        item['info'] = ' '.join(weather_info.xpath('dd[@class="shidu"]/b/text()').extract())
        item['quality'] = weather_info.xpath('dd[@class="kongqi"]/h5/text()').extract_first()
        item['pm'] = weather_info.xpath('dd[@class="kongqi"]/h6/text()').extract_first()
        item['sun_up_down'] = ' '.join(weather_info.xpath('dd[@class="kongqi"]/span/text()').extract())
        item['date_info'] = weather_info.xpath('dd[@class="week"]/text()').extract_first()
        return item


if __name__ == '__main__':
    from scrapy import cmdline

    name = WeatherSpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
