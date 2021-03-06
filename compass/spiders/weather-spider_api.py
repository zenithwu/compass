# -*- coding: utf-8 -*-
import os

import scrapy
import json
import time

from compass.items import CompassItem


class WeatherSpider(scrapy.Spider):
    name = 'weather-spider-api'
    start_urls = [
        'https://restapi.amap.com/v3/config/district?key=19ca317cf68842316570c533f108ba0a&subdistrict=3',
    ]
    data_path = os.path.join("../data/")
    weather_url = 'https://restapi.amap.com/v3/weather/weatherInfo?key=19ca317cf68842316570c533f108ba0a&extensions=all&city='
    custom_settings = {
        'ITEM_PIPELINES': {
            'compass.pipelines.JsonLinesExporterPipeline': 1
        }
    }

    def parse(self, response):
        obj = json.loads(response.text)
        for provicne in obj['districts'][0]['districts']:
            for city in provicne['districts']:
                time.sleep(0.1)
                yield scrapy.Request(url=self.weather_url + city.get('adcode', '')
                                     , callback=self.parse_weather)
                for area in city['districts']:
                    time.sleep(0.1)
                    yield scrapy.Request(url=self.weather_url + area.get('adcode', '')
                                         , callback=self.parse_weather)

    def parse_weather(self, response):
        item = CompassItem()
        item["info"] = json.loads(response.text)
        return item


if __name__ == '__main__':
    from scrapy import cmdline

    name = WeatherSpider().name
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
