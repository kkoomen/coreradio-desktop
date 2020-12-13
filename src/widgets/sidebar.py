#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from widgets.home_feed import HomeFeed
from signals import PageSignal
from utils import clickable, css
import colors

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

        self.register_menu_item('Home', 'home', HomeFeed)

        self.layout.addWidget(self.scrollarea)
        self.setLayout(self.layout)

    def register_menu_item(self, text, icon, page):
        menu_item_widget = QWidget()
        menu_item_widget.setObjectName(u'menu_item_widget')
        menu_item_widget_layout = QHBoxLayout(alignment=Qt.AlignLeft)
        menu_item_widget.setLayout(menu_item_widget_layout)
        menu_item_widget.setStyleSheet(css(
            '''
            #menu_item_widget {
                border-radius: 8px;
                background-color: transparent;
                background-color: {{secondaryColor}};
            }
            #menu_item_widget:hover {
                background-color: {{primaryColor}};
            }
            QLabel {
                background-color: transparent;
            }
            ''',
            secondaryColor=colors.SECONDARY_COLOR,
            primaryColor=colors.PRIMARY_COLOR
        ))

        clickable(menu_item_widget).connect(lambda: PageSignal.changed.emit(page()))

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(':/icons/24x24/{}'.format(icon)).pixmap(24))
        menu_item_widget_layout.addWidget(icon_label)
        menu_item_widget_layout.addWidget(QLabel(text))
        self.flow_layout.addWidget(menu_item_widget)
