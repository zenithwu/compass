# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompassItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    index = scrapy.Field()
    name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    temperature = scrapy.Field()
    weather = scrapy.Field()
    info = scrapy.Field()
    quality = scrapy.Field()
    pm = scrapy.Field()
    sun_up_down = scrapy.Field()
    date_info = scrapy.Field()

    # pass
