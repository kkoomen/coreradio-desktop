#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""

import sys
from PySide2.QtWidgets import QApplication, QHBoxLayout, QWidget
from widgets.sidebar import Sidebar
from widgets.page_content import PageContent

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("CORERADIO")
        self.resize(1353, 800)

        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(0)
        self.layout.addWidget(Sidebar())
        self.layout.addWidget(PageContent())
        self.setLayout(self.layout)


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
