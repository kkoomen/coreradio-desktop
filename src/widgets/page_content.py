#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QVBoxLayout
from widgets.home_feed import HomeFeed
from signals import PageSignal

class PageContent(QWidget):

    def __init__(self):
        super(PageContent, self).__init__()
        PageSignal.changed.connect(self.on_change_page)

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.layout.addWidget(HomeFeed())
        self.setLayout(self.layout)

    @Slot(QWidget)
    def on_change_page(self, widget):
        current = self.layout.takeAt(0)
        w = current.widget()
        w.setParent(None)
        self.layout.addWidget(widget)
