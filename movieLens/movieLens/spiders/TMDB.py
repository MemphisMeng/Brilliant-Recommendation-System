# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from movieLens.items import MovielensItem


class TmdbSpider(scrapy.Spider):
    name = 'TMDB'
    allowed_domains = ['themoviedb.org']
    start_urls = ['https://www.themoviedb.org/movie/']
    movie_codes = pd.read_csv('movie_code.csv')['id']

    def start_requests(self):
        for code in self.movie_codes:
            yield scrapy.Request(url=self.start_urls[0] + str(int(code)),
                                 callback=self.parse, dont_filter=True,
                                 meta={'id': code})

    def parse(self, response):
        item = MovielensItem()
        item['id'] = response.meta['id']
        link = response.xpath('//div[@class="image_content backdrop"]/img/@data-src').extract_first(default='')
        item['poster'] = link
        yield item
