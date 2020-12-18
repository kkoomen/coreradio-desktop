#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Signal, QEvent, QObject
from constants import SETTINGS_FILE, DOWNLOAD_HISTORY_FILE
from datetime import datetime
import re
import json
import math


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


def replace_multiple(text, replacements):
    result = text
    for regex, sub in replacements:
        result = re.sub(regex, sub, result)
    return result


def get_settings():
    try:
        return json.loads(open(SETTINGS_FILE, 'r').read())
    except Exception as e:
        return {}


def get_download_history():
    try:
        return json.loads(open(DOWNLOAD_HISTORY_FILE, 'r').read())
    except Exception as e:
        return []


def update_download_history(item):
    history = get_download_history()
    for index, download_item in enumerate(history):
        if download_item['id'] == item['id']:
            history[index] = item
    with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
        json.dump(history, f)
        f.close()


def timeago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    else:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(math.floor(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(math.floor(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(math.floor(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(math.floor(day_diff)) + " days ago"
    if day_diff < 31:
        return str(math.floor(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(math.floor(day_diff / 30)) + " months ago"
    return str(math.floor(day_diff / 365)) + " years ago"
