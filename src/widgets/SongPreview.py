#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QImage, QPixmap
from helpers.RunThread import RunThread
import time
import requests

class SongPreview(QWidget):

    def __init__(self, **kwargs):
        super(SongPreview, self).__init__()
        self.image_size = 300
        self.thread = RunThread(self.fetch_image, self.on_image_loaded)

        self.layout = QVBoxLayout()
        self.image = kwargs['image']
        self.title = kwargs['title']

        self.image_label = QLabel()
        self.image_label.setMinimumWidth(self.image_size)
        self.image_label.setMinimumHeight(self.image_size)
        self.layout.addWidget(self.image_label)

        title = QLabel(self.title)
        title.setWordWrap(True)
        self.layout.addWidget(title)

        self.setLayout(self.layout)

    def fetch_image(self):
        time.sleep(1)
        response = requests.get(self.image)
        self.image_content = response.content
        return True

    def on_image_loaded(self):
        imgWidget = QImage()
        imgWidget.loadFromData(self.image_content)
        picture = QPixmap(imgWidget)
        picture = picture.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)
        self.image_label.setPixmap(picture)
