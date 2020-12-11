#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

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

        label = QLabel('Home')
        label.setStyleSheet('background-color: none;')
        self.flow_layout.addWidget(label)

        self.layout.addWidget(self.scrollarea)
        self.setLayout(self.layout)
