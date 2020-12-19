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
from constants import CONFIG_DIR, ARTWORK_DIR, DOWNLOAD_HISTORY_FILE
from utils import get_download_history
import os
import resources_rc
import json


if not os.path.exists(CONFIG_DIR):
    print('Creating new config directory at {}'.format(CONFIG_DIR))
    os.mkdir(CONFIG_DIR)

if not os.path.exists(ARTWORK_DIR):
    print('Creating new artwork directory at {}'.format(ARTWORK_DIR))
    os.mkdir(ARTWORK_DIR)


# Allow the ones that are not 100% downloaded to be re-downloaded
history = get_download_history()
for index, item in enumerate(history):
    if item['progress'] != 100:
        history[index] = { **item, 'retriable': True }
with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
    json.dump(history, f)
    f.close()


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
