#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel
from widgets.home_feed import HomeFeed
from widgets.downloads import Downloads
from widgets.user_settings import UserSettings
from widgets.buttons import IconButton
from signals import PageSignal
from utils import get_download_history, css
from signals import DownloadHistorySignal
import re
import colors


class Sidebar(QWidget):

    def __init__(self):
        super(Sidebar, self).__init__()
        DownloadHistorySignal.put.connect(self.update_notification_amount)
        DownloadHistorySignal.progress.connect(self.update_notification_amount)
        self.sidebar_width = 300
        self.setStyleSheet('background: rgba(0, 0, 0, 0.05);');
        self.setFixedWidth(self.sidebar_width)

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget(self.scrollarea)
        self.scrollarea.setWidget(widget)

        self.flow_layout = QVBoxLayout(widget, alignment=Qt.AlignTop)

        self.register_menu_item('Home', icon='home', page=HomeFeed)
        self.register_menu_item('Downloads', icon='download', page=Downloads)
        self.register_menu_item('Settings', icon='cog', page=UserSettings)
        self.render_total_downloads()

        self.layout.addWidget(self.scrollarea)
        self.setLayout(self.layout)

    def render_total_downloads(self):
        total_downloads_label_size = 19
        self.total_downloads_label = QLabel('1', self.downloads_menu_item)
        self.total_downloads_label.setAlignment(Qt.AlignCenter)
        self.total_downloads_label.hide()
        self.total_downloads_label.setFixedWidth(total_downloads_label_size)
        self.total_downloads_label.setFixedHeight(total_downloads_label_size)
        y = self.downloads_menu_item.sizeHint().height() / 2 - round(total_downloads_label_size / 2)
        x = self.sidebar_width - total_downloads_label_size * 3
        self.total_downloads_label.move(x, y)
        self.total_downloads_label.setStyleSheet(css(
            '''
            text-align: center;
            background: {{backgroundColor}};
            padding: 2px;
            border-radius: 9px;
            ''',
            backgroundColor=colors.GREY_COLOR
        ))

    @Slot(dict)
    def update_notification_amount(self):
        history = get_download_history()
        in_progress_items_length = len([item for item in history if item['progress'] != 100])
        self.total_downloads_label.setText(str(in_progress_items_length))
        if in_progress_items_length > 0:
            self.total_downloads_label.show()
        else:
            self.total_downloads_label.hide()

    def register_menu_item(self, text, icon=None, page=None):
        btn = IconButton(icon=icon,
                         text=text,
                         on_click=lambda: PageSignal.changed.emit(page()))
        property_name = '{}_menu_item'.format(re.sub(r'\s+', '_', text).lower())
        setattr(self, property_name, btn)
        self.flow_layout.addWidget(btn)
