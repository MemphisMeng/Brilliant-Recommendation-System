# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from movieLens.items import DownloaderItem


class DownloaderSpider(scrapy.Spider):
    name = 'downloader'
    allowed_domains = ['themoviedb.org']
    start_urls = ['http://themoviedb.org/']
    posters = pd.read_csv('data/posters.csv')
    posters = posters[posters['poster'].notna()]
    movie_code = pd.read_csv('data/movie_code.csv')

    train_set = movie_code[movie_code['genres'].notna()]
    train_set = pd.merge(posters, train_set, left_on='id', right_on='id')
    train_set = train_set.drop(columns=['title', 'genres'])

    test_set = movie_code[movie_code['genres'].isna()]
    test_set = pd.merge(posters, test_set, left_on='id', right_on='id')
    test_set = test_set.drop(columns=['title', 'genres'])

    def parse(self, response):
        item = DownloaderItem()
        images = []

        # test
        for i in range(self.test_set.shape[0]):
            img_url = self.test_set['poster'].iloc[i]
            image_name = str(self.test_set['id'].iloc[i])
            images.append({'url': img_url, 'name': image_name, 'type': 'test'})

        # train
        for i in range(self.train_set.shape[0]):
            img_url = self.train_set['poster'].iloc[i]
            image_name = str(self.train_set['id'].iloc[i])
            images.append({'url': img_url, 'name': image_name, 'type': 'train'})

        item['image_urls'] = images
        yield item
