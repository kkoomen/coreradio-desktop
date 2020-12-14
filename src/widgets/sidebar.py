#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from widgets.home_feed import HomeFeed
from widgets.buttons import IconButton
from widgets.user_settings import UserSettings
from signals import PageSignal

class Sidebar(QWidget):

    def __init__(self):
        super(Sidebar, self).__init__()
        self.setStyleSheet('background: rgba(0, 0, 0, 0.05);');
        self.setFixedWidth(300)

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget(self.scrollarea)
        self.scrollarea.setWidget(widget)

        self.flow_layout = QVBoxLayout(widget, alignment=Qt.AlignTop)

        self.register_menu_item('Home', icon='home', page=HomeFeed)
        self.register_menu_item('Settings', icon='cog', page=UserSettings)

        self.layout.addWidget(self.scrollarea)
        self.setLayout(self.layout)

    def register_menu_item(self, text, icon=None, page=None):
        btn = IconButton(icon=icon,
                         text=text,
                         on_click=lambda: PageSignal.changed.emit(page()))
        self.flow_layout.addWidget(btn)
