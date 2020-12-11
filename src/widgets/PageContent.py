#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from widgets.SongPreview import SongPreview
from widgets.FlowLayout import FlowLayout

content = [
    {
        'image': 'https://e-cdns-images.dzcdn.net/images/cover/482a634a30a55004e1e58c2f1a81d8f2/1400x1400-000000-80-0-0.jpg',
        'title': 'Devil Sold His Soul - Beyond Reach [single] (2020)',
    },
    {
        'image': 'https://e-cdns-images.dzcdn.net/images/cover/6bef00dbe663045f853c5a60442ea7a5/1400x1400-000000-80-0-0.jpg',
        'title': 'Deeds of Flesh - Nucleus (2020)',
    },
    {
        'image': 'https://e-cdns-images.dzcdn.net/images/cover/c31c575437f5294d96f56815a0612838/1400x1400-000000-80-0-0.jpg',
        'title': 'Neon Graves - All That Brings Us Down (2020)',
    },
    {
        'image': 'https://sun9-73.userapi.com/hMGESRhc-7_a2stZijILxw7Aq8T-Kbjp6fNATw/fLRCuO7DdP4.jpg',
        'title': 'Defiler vocalist Jake Shaw needs our help',
    },
    {
        'image': 'https://cdns-images.dzcdn.net/images/cover/e7e8ac3050153da8aeaf94a3f10a4e44/1400x1400-000000-80-0-0.jpg',
        'title': 'Full Bloom - Malware [single] (2020)',
    },
    {
        'image': 'https://sun9-56.userapi.com/impg/D7VylCTBv2qOCdlI7G2ntZghz_0-YYZHfW59Xg/-Nx9WbP3puI.jpg?size=1440x1440&quality=96&proxy=1&sign=1544176ce56a101024a9e09c9168efa0&type=album',
        'title': 'Brand of Sacrifice - Demon King [single] (2020)',
    },
]

class PageContent(QWidget):

    def __init__(self):
        super(PageContent, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        self.page_widget = QScrollArea()
        self.page_widget.setWidgetResizable(True)

        widget = QWidget(self.page_widget)
        widget.setMinimumWidth(350)
        self.page_widget.setWidget(widget)

        self.flow_layout = FlowLayout(widget)

        for item in content:
            preview_widget = SongPreview(image=item['image'], title=item['title'])
            self.flow_layout.addWidget(preview_widget)

        self.layout.addWidget(self.page_widget)
        self.setLayout(self.layout)
