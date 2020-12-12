#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from bs4 import BeautifulSoup
import requests
import json
import re

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

    def get_song_info(self, url=None):
        result = {}
        print('GET {}'.format(url))

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find(id='dle-content')
        if container:
            script_tag = container.select('[type="application/ld+json"]')
            inline_info = json.loads(str(script_tag[0].string))
            result = inline_info['description']
            result['image'] = inline_info['image']
            result['title'] = inline_info['name']

            # Get the song list info
            info_container = container.select('.full-news-info')[0]
            songs = info_container.find_all(string=re.compile(r'\d+\.\s*.+'))
            if len(songs) > 0:
                # Check if this is a full album release or not.
                result['full_release'] = True
                for text in songs:
                    if text.next_sibling.name == 'b':
                        result['full_release'] = False
                        break

                # Add all the songnames to the list.
                result['songlist'] = []
                for text in songs:
                    songname = str(text)
                    released = True if result['full_release'] else False
                    if text.next_sibling.name == 'b':
                        released = True
                        songname += str(text.next_sibling.string)
                    result['songlist'].append({
                        'name': songname.strip(),
                        'released': released
                    })
        return result

    def search(self, keywords=None):
        pass
