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
import requests


class Song(QWidget):

    def __init__(self, song=None):
        super(Song, self).__init__()
        self.song = song

        color = '#fff' if self.song['released'] else '#666'
        self.setStyleSheet(css(
            '''
            QWidget {
                color: {{color}}
            }
            ''',
            color=color
        ))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.addWidget(QLabel(self.song['name']))
        self.setLayout(self.layout)


class Songlist(QWidget):

    def __init__(self, songlist=None):
        super(Songlist, self).__init__()
        self.songlist = songlist

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(25)
        for song in self.songlist:
            self.layout.addWidget(Song(song=song))
        self.setLayout(self.layout)

class SongDetailPage(QWidget):

    def __init__(self, url=None):
        super(SongDetailPage, self).__init__()
        self.url = url
        self.loading = True
        self.song = None
        self.thread = RunThread(self.get_song_info, self.on_song_info)

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
        image_size = 400
        image_label = QLabel()
        image_label.setMinimumWidth(image_size)
        image_label.setMinimumHeight(image_size)
        inner_container_layout.addWidget(image_label, alignment=Qt.AlignTop)

        response = requests.get(self.song['image'])
        imgWidget = QImage()
        imgWidget.loadFromData(response.content)
        picture = QPixmap(imgWidget)
        picture = picture.scaled(image_size, image_size, Qt.KeepAspectRatio)
        image_label.setPixmap(picture)

        # Songlist
        inner_container_layout.addWidget(
            Songlist(songlist=self.song['songlist']),
            alignment=Qt.AlignTop)

    def get_song_info(self):
        spider = CoreRadioSpider()
        self.song = spider.get_song_info(url=self.url)
        return True

    def on_song_info(self):
        if self.song is not None:
            self.render_song_info()
            self.loading = False
        else:
            self.page_layout.addWidget(QLabel("Something wen't wrong"))
