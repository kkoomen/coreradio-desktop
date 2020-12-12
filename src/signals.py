#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget

class Page(QObject):
    changed = Signal(QWidget)
PageSignal = Page()
