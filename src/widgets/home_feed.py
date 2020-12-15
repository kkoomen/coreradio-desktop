#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel
from widgets.song_preview import SongPreview
from widgets.flow_layout import FlowLayout
from widgets.run_thread import RunThread
from spider import CoreRadioSpider


class HomeFeed(QWidget):

    def __init__(self):
        super(HomeFeed, self).__init__()
        self.run_get_feed_thread()

        self.feed = []
        self.page = 1
        self.loading = False

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        self.page_widget = QScrollArea()
        self.page_widget.setWidgetResizable(True)
        self.page_widget.viewport().installEventFilter(self)

        widget = QWidget(self.page_widget)
        widget.setMinimumWidth(350)
        self.page_widget.setWidget(widget)

        self.flow_layout = FlowLayout(widget)
        self.flow_layout.setContentsMargins(25, 25, 25, 25)

        self.layout.addWidget(self.page_widget)
        self.setLayout(self.layout)

    def run_get_feed_thread(self):
        self.thread = RunThread(self.get_feed, self.on_feed_receive)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.Wheel and source is self.page_widget.viewport() and not self.loading):
            scrollbar = self.page_widget.verticalScrollBar()
            y = scrollbar.value()
            bottom = scrollbar.maximum()
            if y >= bottom:
                self.page += 1
                self.loading = True
                self.run_get_feed_thread()
        return super(HomeFeed, self).eventFilter(source, event)

    def get_feed(self):
        spider = CoreRadioSpider()
        self.feed = spider.get_home_feed(page=self.page)
        return True

    def on_feed_receive(self):
        if len(self.feed) > 0:
            for item in self.feed:
                preview_widget = SongPreview(image=item['image'],
                                             title=item['title'],
                                             url=item['href'])
                self.flow_layout.addWidget(preview_widget)
                self.loading = False
        else:
            self.flow_layout.addWidget(QLabel("Something wen't wrong"))
