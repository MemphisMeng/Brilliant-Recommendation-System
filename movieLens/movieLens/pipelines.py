# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem


class MovielensPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomedImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image in item['image_urls']:
            yield scrapy.Request(image['url'], meta={'image_name': image['name'], 'type': image['type']})

    def file_path(self, request, response=None, info=None):
        if request.meta['type'] == 'test':
            return "/test/%s.jpg" % request.meta['image_name']
        else:
            return "/train/%s.jpg" % request.meta['image_name']