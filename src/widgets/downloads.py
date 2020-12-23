#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QStackedLayout
from PySide2.QtGui import QPixmap, QFont
from utils import get_download_history, css, timeago, download_song, update_download_history
from widgets.run_thread import RunThread
from widgets.buttons import IconButton
from signals import DownloadHistorySignal
from constants import DOWNLOAD_HISTORY_FILE
import colors
import json
import os
import logging


class DownloadItem(QWidget):

    def __init__(self, item=None):
        super(DownloadItem, self).__init__()
        DownloadHistorySignal.put.connect(self.update)
        DownloadHistorySignal.progress.connect(self.update)
        self.artwork_size = 80
        self.item = item
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        item_container = QWidget()
        item_container_layout = QHBoxLayout()
        item_container_layout.setMargin(0)
        item_container.setLayout(item_container_layout)

        self.artwork_label = QLabel(alignment=Qt.AlignLeft)
        self.artwork_label.setStyleSheet(css('background-color: {{color}};', color=colors.PLACEHOLDER_COLOR))
        self.artwork_label.setFixedWidth(self.artwork_size)
        self.artwork_label.setFixedHeight(self.artwork_size)
        item_container_layout.addWidget(self.artwork_label)
        self.render_artwork()

        self.item_label = QLabel(self.get_text())
        font = QFont()
        font.setKerning(False)
        self.item_label.setFont(font)
        self.item_label.setStyleSheet('padding: 0 10px;')
        item_container_layout.addWidget(self.item_label)

        self.retry_btn = IconButton(text='Retry', on_click=self.retry)
        self.retry_btn.setFixedHeight(40)
        self.retry_btn.setFixedWidth(60)
        item_container_layout.addWidget(self.retry_btn)
        if not self.item['retriable']:
            self.retry_btn.hide()


        delete_btn = IconButton(text='Delete', on_click=self.delete)
        delete_btn.setFixedHeight(40)
        delete_btn.setFixedWidth(70)
        item_container_layout.addWidget(delete_btn)

        self.layout.addWidget(item_container)

        self.progress_label = QLabel()
        self.layout.addWidget(self.progress_label)

        self.setLayout(self.layout)

    def retry(self):
        thread_id = 'download_thread_{}'.format(self.item['id'])
        setattr(self, thread_id, RunThread(download_song, None, self.item))

    def render_artwork(self):
        if os.path.exists(self.item['artwork_local_path']):
            picture = QPixmap(self.item['artwork_local_path'])
            picture = picture.scaled(self.artwork_size, self.artwork_size, Qt.KeepAspectRatio)
            self.artwork_label.setPixmap(picture)

    def get_text(self):
        downloadColor = '#FF9800' if self.item['progress'] < 100 else '#4CAF50';
        return css(
            '<span style="color: {{downloadColor}};">({}%)</span> {}<br/><span style="color:#888;"><br/>Saved as {}/{}<br/>{} • {}</span>',
            downloadColor=downloadColor
        ).format(
            self.item['progress'],
            self.item['title'],
            self.item['location'],
            self.item['filename'],
            self.item['quality'],
            timeago(self.item['created'])
        )

    def delete(self):
        filepath ='{}/{}'.format(self.item['location'], self.item['filename'])
        if os.path.exists(filepath):
            logging.info('Deleting downloaded file: {}'.format(filepath))
            os.remove(filepath)

        if os.path.exists(self.item['artwork_local_path']):
            logging.info('Deleting artwork in {}'.format(self.item['artwork_local_path']))
            os.remove(self.item['artwork_local_path'])

        history = get_download_history()
        filtered_history = [item for item in history if item['id'] != self.item['id']]
        with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
            json.dump(filtered_history, f)
            f.close()
            self.setParent(None)

    @Slot(dict)
    def update(self, item):
        if self.item['id'] == item['id']:
            self.item = item
            self.item_label.setText(self.get_text())
            self.render_artwork()

            if item['retriable']:
                self.retry_btn.hide()
                update_download_history({ **item, 'retriable': False })


class Downloads(QWidget):

    def __init__(self):
        super(Downloads, self).__init__()
        self.history = get_download_history()
        self.history.reverse()

        self.layout = QStackedLayout()
        self.layout.setMargin(0)

        self.page_widget = QScrollArea()
        self.page_widget.setWidgetResizable(True)

        widget = QWidget(self.page_widget)
        widget.setMinimumWidth(350)
        self.page_widget.setWidget(widget)

        self.page_layout = QVBoxLayout(widget, alignment=Qt.AlignTop)
        self.page_layout.setMargin(0)
        self.page_layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setCurrentWidget(self.page_widget)

        if len(self.history) == 0:
            self.history_empty_label = QLabel('No downloads', alignment=Qt.AlignCenter)
            self.layout.addWidget(self.history_empty_label)
            self.layout.setCurrentWidget(self.history_empty_label)

        for item in self.history:
            self.page_layout.addWidget(DownloadItem(item=item))

        self.layout.addWidget(self.page_widget)
        self.setLayout(self.layout)
