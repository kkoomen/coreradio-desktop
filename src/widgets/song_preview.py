#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QImage, QPixmap
from widgets.run_thread import RunThread
from widgets.song_detail_page import SongDetailPage
from signals import PageSignal
from utils import clickable, css
import time
import requests
import colors

class SongPreview(QWidget):

    def __init__(self, **kwargs):
        super(SongPreview, self).__init__()
        self.artwork_content = None
        self.artwork_size = 300
        self.artwork = kwargs['artwork']
        self.title = kwargs['title']
        self.url = kwargs['url']

        if self.artwork is not None:
            self.thread = RunThread(self.fetch_artwork, self.on_artwork_loaded)

        self.layout = QVBoxLayout()

        self.artwork_label = QLabel()
        self.artwork_label.setStyleSheet(css('background-color: {{color}};', color=colors.PLACEHOLDER_COLOR))
        self.artwork_label.setFixedWidth(self.artwork_size)
        self.artwork_label.setFixedHeight(self.artwork_size)
        clickable(self.artwork_label).connect(self.on_click)
        self.layout.addWidget(self.artwork_label)

        title = QLabel(self.title)
        title.setWordWrap(True)
        title.setFixedWidth(300)
        self.layout.addWidget(title)

        self.setLayout(self.layout)

    def on_click(self):
        PageSignal.changed.emit(SongDetailPage(url=self.url))

    def fetch_artwork(self):
        time.sleep(1)
        print('GET {}'.format(self.artwork))
        try:
            response = requests.get(self.artwork)
            self.artwork_content = response.content
        except Exception:
            return False
        return True

    def on_artwork_loaded(self):
        if self.artwork_content:
            imgWidget = QImage()
            imgWidget.loadFromData(self.artwork_content)
            picture = QPixmap(imgWidget)
            picture = picture.scaled(self.artwork_size, self.artwork_size, Qt.KeepAspectRatio)
            self.artwork_label.setPixmap(picture)
            print('[DONE] GET {}'.format(self.artwork))
        else:
            print('[FAILED] GET {}'.format(self.artwork))
