#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from bs4 import BeautifulSoup
import requests

class CoreRadioSpider:

    def __init__(self):
        self.BASE_URL = 'https://coreradio.ru'

    def url(self, path=''):
        return '{}{}'.format(self.BASE_URL, path)

    def get_home_feed(self, page=1):
        feed = []

        url = self.url('/page/{}'.format(page))
        print('GET {}'.format(url))

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find(id='dle-content')
        if container:
            for item in container.select('.tcarusel-item'):
                image_path = item.select('.tcarusel-item-image img')[0].get('src')
                feed.append({
                    'image': image_path if not 'no_image' in image_path else None,
                    'title': str(item.select('.tcarusel-item-title a')[0].string).strip(),
                    'href': item.select('.tcarusel-item-title a')[0].get('href'),
                })
        return feed

    def search(self, keywords=None):
        pass
