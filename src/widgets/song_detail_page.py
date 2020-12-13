#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy
from PySide2.QtGui import QImage, QPixmap
from widgets.run_thread import RunThread
from spider import CoreRadioSpider
from typography import H1
from utils import css
import time
import requests


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


class SongDetailPage(QWidget):

    def __init__(self, url=None):
        super(SongDetailPage, self).__init__()
        self.url = url
        self.loading = False
        self.image_content = None
        self.image_size = 400
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
        # Title
        title = H1(self.song['title'])
        title.setWordWrap(True)
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
        self.image_label = QLabel()
        self.image_label.setStyleSheet('background-color: #252525;')
        self.image_label.setMinimumWidth(self.image_size)
        self.image_label.setMinimumHeight(self.image_size)
        inner_container_layout.addWidget(self.image_label, alignment=Qt.AlignTop)
        self.get_image_thread = RunThread(self.fetch_image, self.on_image_loaded)

        # Songlist
        inner_container_layout.addWidget(
            Songlist(songlist=self.song['songlist']),
            alignment=Qt.AlignTop)

    def fetch_image(self):
        time.sleep(1)
        print('GET {}'.format(self.song['image']))
        response = requests.get(self.song['image'])
        self.image_content = response.content
        return True

    def on_image_loaded(self):
        if self.image_content:
            imgWidget = QImage()
            imgWidget.loadFromData(self.image_content)
            picture = QPixmap(imgWidget)
            picture = picture.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)
            self.image_label.setPixmap(picture)
            print('[DONE] GET {}'.format(self.song['image']))
        else:
            print('[FAILED] GET {}'.format(self.song['image']))

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
