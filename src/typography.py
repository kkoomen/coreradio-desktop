#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel

class Heading(QLabel):

    def __init__(self, *args, **kwargs):
        super(Heading, self).__init__(*args, **kwargs)
        self.font = QFont()
        self.font.setWeight(75)
        self.font.setBold(True)

class H1(Heading):

    def __init__(self, *args, **kwargs):
        super(H1, self).__init__(*args, **kwargs)
        self.font.setPointSize(34)
        self.setFont(self.font)

class H2(Heading):

    def __init__(self, *args, **kwargs):
        super(H2, self).__init__(*args, **kwargs)
        self.font.setPointSize(30)
        self.setFont(self.font)
