# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import os
import time


# 此piplines将结果导成多个json记录到文件中
class JsonLinesExporterPipeline:
    file = None
    exporter = None

    def open_spider(self, spider):
        # 初始化 exporter 实例，执行输出的文件和编码
        data_path = os.path.join("../data/", time.strftime('%Y-%m-%d', time.localtime()))
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        self.file = open(os.path.join(data_path, spider.name + '.json'), 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)

    def close_spider(self, spider):
        self.file.close()
        # 将 Item 实例导出到 json 文件

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
