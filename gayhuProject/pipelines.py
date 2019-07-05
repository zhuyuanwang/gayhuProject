# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 不需要经过管道，直接在爬虫文件中下载文件。
# 那就备注一句：湖人总冠军
class GayhuprojectPipeline(object):
    def process_item(self, item, spider):
        return item
