#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from PySide2.QtGui import QImage, QPixmap
from widgets.run_thread import RunThread
from widgets.buttons import IconButton
from spider import CoreRadioSpider
from typography import H2
from utils import css, get_settings, replace_multiple, get_download_history, update_download_history, download_song
from signals import DownloadHistorySignal
from constants import DOWNLOAD_HISTORY_FILE, ARTWORK_DIR
import colors
import time
import requests
import json
import os
from uuid import uuid4
from datetime import datetime


class Song(QWidget):

    def __init__(self, song=None, index=None):
        super(Song, self).__init__()
        self.song = song

        color = '#fff' if self.song['released'] else '#666'
        self.setStyleSheet(css('color: {{color}};', color=color))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        label = '{}.  {}'.format(index, self.song['name'])
        self.layout.addWidget(QLabel(label))
        self.setLayout(self.layout)


class Songlist(QWidget):

    def __init__(self, songlist=None):
        super(Songlist, self).__init__()
        self.songlist = songlist

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(25)
        for index, song in enumerate(self.songlist):
            self.layout.addWidget(Song(song=song, index=index+1))
        self.setLayout(self.layout)


class Header(QWidget):

    def __init__(self, song=None):
        super(Header, self).__init__()
        self.song = song
        self.settings = get_settings()
        self.layout = QGridLayout()
        self.layout.setMargin(0)
        self.layout.setContentsMargins(0, 0, 0, 25)

        self.setObjectName(u'header')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(css(
            '''
            #header {
                border-bottom: 1px solid {{backgroundColor}};
            }
            ''',
            backgroundColor=colors.SECONDARY_COLOR
        ))

        self.left_container = QWidget()
        self.left_container.setStyleSheet(css('color: {{color}};', color=colors.GREY_COLOR))
        self.left_container_layout = QHBoxLayout(alignment=Qt.AlignLeft)
        self.left_container_layout.setMargin(0)
        self.left_container.setLayout(self.left_container_layout)

        self.right_container = QWidget()
        self.right_container_layout = QHBoxLayout(alignment=Qt.AlignRight)
        self.right_container_layout.setMargin(0)
        self.right_container.setLayout(self.right_container_layout)

        self.layout.addWidget(self.left_container, 0, 0)
        self.layout.addWidget(self.right_container, 0, 1)

        # Info on the left
        info_text = '{} · {} songs'.format(self.song['genre'], len(self.song['songlist'])).upper()
        self.left_container_layout.addWidget(QLabel(info_text))

        # Download buttons on the right
        if 'download_links' in self.song:
            for item in self.song['download_links']:
                btn = IconButton(text=item['label'],
                                 icon='download',
                                 on_click=self.download(item))
                self.right_container_layout.addWidget(btn)

        self.setLayout(self.layout)

    def download(self, link):
        def closure():
            filename = replace_multiple(self.song['title'], (
                (r'\s+', '_'),
                (r'[^\w]+', ''),
                (r'_+', '_'),
            )).lower()
            self.start_download_thread({
                'id': str(uuid4()),
                'url': link['url'],
                'title': self.song['title'],
                'artwork_local_path': '{}/{}.jpg'.format(ARTWORK_DIR, filename),
                'artwork_url': self.song['artwork'],
                'quality': link['label'],
                'filename': '{}.tar'.format(filename),
                'basename': filename,
                'location': self.settings['file_storage_location'],
                'progress': 0,
                'created': int(datetime.now().strftime('%s'))
            })
        return closure

    def start_download_thread(self, item):
        print('Starting download thread: {}'.format(item['id']))
        thread_id = 'download_thread_{}'.format(item['id'])
        history = get_download_history()
        history.append(item)
        with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
            json.dump(history, f)
            f.close()
        setattr(self, thread_id, RunThread(download_song, None, item))


class SongDetailPage(QWidget):

    def __init__(self, url=None):
        super(SongDetailPage, self).__init__()
        self.url = url
        self.loading = False
        self.artwork_content = None
        self.artwork_size = 400
        self.song = None

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        self.page_widget = QScrollArea()
        self.page_widget.setWidgetResizable(True)

        widget = QWidget(self.page_widget)
        widget.setMinimumWidth(800)
        self.page_widget.setWidget(widget)

        self.page_layout = QVBoxLayout(widget, alignment=Qt.AlignTop)
        self.page_layout.setContentsMargins(25, 25, 25, 25)

        self.layout.addWidget(self.page_widget)
        self.setLayout(self.layout)

        self.thread = RunThread(self.get_song_info, self.on_song_info)

    def render_song_info(self):
        # Header
        self.page_layout.addWidget(Header(song=self.song))

        # Title
        title = H2(self.song['title'])
        title.setWordWrap(True)
        title.setStyleSheet('padding-top: 20px;')
        self.page_layout.addWidget(title)

        # Inner container that contains Image + Songlist
        inner_container = QWidget()
        inner_container_layout = QHBoxLayout(alignment=Qt.AlignTop|Qt.AlignLeft)
        inner_container_layout.setMargin(0)
        inner_container_layout.setSpacing(25)
        inner_container_layout.setContentsMargins(0, 25, 0, 0)
        inner_container.setLayout(inner_container_layout)
        self.page_layout.addWidget(inner_container)

        # Image
        self.artwork_label = QLabel()
        self.artwork_label.setStyleSheet(css('background-color: {{color}};', color=colors.PLACEHOLDER_COLOR))
        self.artwork_label.setFixedWidth(self.artwork_size)
        self.artwork_label.setFixedHeight(self.artwork_size)
        inner_container_layout.addWidget(self.artwork_label, alignment=Qt.AlignTop)
        self.get_artwork_thread = RunThread(self.fetch_artwork, self.on_artwork_loaded)

        # Songlist
        inner_container_layout.addWidget(
            Songlist(songlist=self.song['songlist']),
            alignment=Qt.AlignTop)

    def fetch_artwork(self):
        time.sleep(1)
        print('GET {}'.format(self.song['artwork']))
        try:
            response = requests.get(self.song['artwork'])
            self.artwork_content = response.content
        except Exception:
            return True
        return True

    def on_artwork_loaded(self):
        if self.artwork_content:
            imgWidget = QImage()
            imgWidget.loadFromData(self.artwork_content)
            picture = QPixmap(imgWidget)
            picture = picture.scaled(self.artwork_size, self.artwork_size, Qt.KeepAspectRatio)
            self.artwork_label.setPixmap(picture)
            print('[DONE] GET {}'.format(self.song['artwork']))
        else:
            print('[FAILED] GET {}'.format(self.song['artwork']))

    def get_song_info(self):
        self.loading = True
        spider = CoreRadioSpider()
        self.song = spider.get_song_info(url=self.url)
        return True

    def on_song_info(self):
        if self.song is not None:
            self.render_song_info()
            self.loading = False
        else:
            self.page_layout.addWidget(QLabel("Something wen't wrong"))
