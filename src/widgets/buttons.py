#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget
from utils import clickable, css
import colors

class IconButton(QWidget):

    def __init__(self,
                 text=None,
                 icon=None,
                 on_click=None,
                 defaultColor=colors.SECONDARY_COLOR,
                 hoverColor=colors.PRIMARY_COLOR):
        super(IconButton, self).__init__()
        clickable(self).connect(on_click)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName(u'button')
        self.layout = QHBoxLayout(alignment=Qt.AlignLeft)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(':/icons/24x24/{}'.format(icon)).pixmap(24))

        self.layout.addWidget(icon_label)
        self.layout.addWidget(QLabel(text))

        self.setStyleSheet(css(
            '''
            #button {
                border-radius: 8px;
                background-color: transparent;
                background-color: {{defaultColor}};
            }
            #button:hover {
                background-color: {{hoverColor}};
            }
            QLabel {
                background-color: transparent;
            }
            ''',
            defaultColor=defaultColor,
            hoverColor=hoverColor
        ))

        self.setLayout(self.layout)
