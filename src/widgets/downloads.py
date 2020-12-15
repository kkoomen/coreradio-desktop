#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from utils import get_download_history
from widgets.buttons import IconButton
from signals import DownloadHistorySignal
from constants import DOWNLOAD_HISTORY_FILE
import json
import os


class DownloadItem(QWidget):

    def __init__(self, item=None):
        super(DownloadItem, self).__init__()
        DownloadHistorySignal.progress.connect(self.update_progress)
        self.item = item
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        item_container = QWidget()
        item_container_layout = QHBoxLayout()
        item_container_layout.setMargin(0)
        item_container.setLayout(item_container_layout)

        self.item_label = QLabel(self.getText())
        self.item_label.setStyleSheet(
            '''
            QLabel {
                padding: 20px;
                background: #444;
                border-radius: 8px;
            }
            '''
        )
        item_container_layout.addWidget(self.item_label)

        delete_btn = IconButton(text='Delete', on_click=self.delete)
        delete_btn.setFixedWidth(100)
        item_container_layout.addWidget(delete_btn)

        self.layout.addWidget(item_container)

        self.progress_label = QLabel()
        self.layout.addWidget(self.progress_label)

        self.setLayout(self.layout)

    def getText(self):
        return '{}% {}'.format(self.item['progress'], self.item['title'])

    def delete(self):
        filepath ='{}/{}'.format(self.item['location'], self.item['filename'])
        if os.path.exists(filepath):
            print('Deleting downloaded file: {}'.format(filepath))
            os.remove(filepath)

        history = get_download_history()
        filtered_history = [item for item in history if item['id'] != self.item['id']]
        with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
            json.dump(filtered_history, f)
            f.close()
            self.setParent(None)

    @Slot(dict)
    def update_progress(self, item):
        if self.item['id'] == item['id']:
            self.item = item
            self.item_label.setText(self.getText())

            history = get_download_history()
            for index, download_item in enumerate(history):
                if download_item['id'] == item['id']:
                    history[index] = item
            with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
                json.dump(history, f)
                f.close()


class Downloads(QWidget):

    def __init__(self):
        super(Downloads, self).__init__()
        self.history = get_download_history()
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        self.page_widget = QScrollArea()
        self.page_widget.setWidgetResizable(True)

        widget = QWidget(self.page_widget)
        widget.setMinimumWidth(350)
        self.page_widget.setWidget(widget)

        self.page_layout = QVBoxLayout(widget, alignment=Qt.AlignTop)
        self.page_layout.setMargin(0)
        self.page_layout.setContentsMargins(25, 25, 25, 25)

        for item in self.history:
            self.page_layout.addWidget(DownloadItem(item=item))

        self.layout.addWidget(self.page_widget)
        self.setLayout(self.layout)
