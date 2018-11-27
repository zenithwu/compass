# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompassItem(scrapy.Item):
    # define the fields for your item here like:
    info = scrapy.Field()
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
class AreaItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    province_id = scrapy.Field()
    province_name = scrapy.Field()
    city_id = scrapy.Field()
    city_name = scrapy.Field()

class PriceItem(scrapy.Item):
    # define the fields for your item here like:
    t_name=scrapy.Field()
    name=scrapy.Field()

    price_type=scrapy.Field()
    price=scrapy.Field()
    price_reportime=scrapy.Field()
    company=scrapy.Field()

class FlightItem(scrapy.Item):
    # define the fields for your item here like:
    start=scrapy.Field()
    end=scrapy.Field()
    info=scrapy.Field()
    no=scrapy.Field()
    start_time=scrapy.Field()
    start_position=scrapy.Field()
    end_time=scrapy.Field()
    end_position=scrapy.Field()
    status=scrapy.Field()
    stat_date=scrapy.Field()