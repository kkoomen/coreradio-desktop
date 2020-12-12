#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Signal, QEvent, QObject
import re

def clickable(widget):
    class Filter(QObject):
        clicked = Signal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def css(text, **replacements):
    result = text
    errors = []
    for key in replacements:
        token = '{{' + key + '}}'
        if re.search(token, result) is None:
            errors.append('Token "{}" does not exists in text'.format(key))
        else:
            result = re.sub(token, replacements[key], result)
    if len(errors) > 0:
        print('CSS replacements resulted into errors')
        print('')
        print(text)
        print('')
        for index, err in enumerate(errors):
            print('{}. {}'.format(index + 1, err))
    return result
