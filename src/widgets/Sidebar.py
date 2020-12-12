#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from widgets.home_feed import HomeFeed
from utils import clickable
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

        self.register_menu_item('Home', HomeFeed)

        self.layout.addWidget(self.scrollarea)
        self.setLayout(self.layout)

    def register_menu_item(self, label, page):
        label = QLabel(label)
        label.setStyleSheet(
            '''
            QLabel {
                padding: 20px;
                border-radius: 8px;
                background-color: transparent;
            }
            QLabel:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            '''
        )
        clickable(label).connect(lambda: PageSignal.changed.emit(page()))
        self.flow_layout.addWidget(label)
