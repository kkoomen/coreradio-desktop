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
from utils import clickable
import time
import requests

class SongPreview(QWidget):

    def __init__(self, **kwargs):
        super(SongPreview, self).__init__()
        self.image_content = None
        self.image_size = 300
        self.image = kwargs['image']
        self.title = kwargs['title']
        self.url = kwargs['url']

        if self.image is not None:
            self.thread = RunThread(self.fetch_image, self.on_image_loaded)

        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setStyleSheet('background-color: rgba(0, 0, 0, 0.1);')
        self.image_label.setMinimumWidth(self.image_size)
        self.image_label.setMinimumHeight(self.image_size)
        clickable(self.image_label).connect(self.on_click)
        self.layout.addWidget(self.image_label)

        title = QLabel(self.title)
        title.setWordWrap(True)
        title.setFixedWidth(300)
        self.layout.addWidget(title)

        self.setLayout(self.layout)

    def on_click(self):
        PageSignal.changed.emit(SongDetailPage(url=self.url))

    def fetch_image(self):
        time.sleep(1)
        response = requests.get(self.image)
        self.image_content = response.content
        return True

    def on_image_loaded(self):
        if self.image_content:
            imgWidget = QImage()
            imgWidget.loadFromData(self.image_content)
            picture = QPixmap(imgWidget)
            picture = picture.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)
            self.image_label.setPixmap(picture)
            print('GET {}'.format(self.image))
        else:
            print('[FAILED] GET {}'.format(self.image))
