# -*- coding: utf-8 -*-

import os

from scrapy.exporters import JsonItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter


# 此piplines将结果导成多个json记录到文件中
class JsonLinesExporterPipeline:
    file = None
    exporter = None

    def open_spider(self, spider):
        # 初始化 exporter 实例，执行输出的文件和编码
        data_path =spider.data_path
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        self.file = open(os.path.join(data_path, spider.name + '.json'), 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)

    def close_spider(self, spider):
        self.file.close()
        # 将 Item 实例导出到 json 文件

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonExporterPipeline:
    # 调用 scrapy 提供的 json exporter 导出 json 文件
    def open_spider(self, spider):
        data_path =spider.data_path
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        self.file = open(os.path.join(data_path, spider.name + '.json'), 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
