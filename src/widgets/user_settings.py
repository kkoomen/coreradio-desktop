#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel, QFileDialog, QDialog
from utils import css, clickable
from signals import UserSettingsSignal
import colors
import os


class FieldLabel(QLabel):

    def __init__(self, text):
        super(FieldLabel, self).__init__(text.upper())
        self.setStyleSheet(css('color: {{color}};', color=colors.GREY_COLOR))


class FileStorageLocation(QWidget):

    def __init__(self, settings):
        super(FileStorageLocation, self).__init__()
        self.settings = settings
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        self.layout.addWidget(FieldLabel('File Storage Location'))

        self.file_field = QLabel(self.settings['file_storage_location'])
        self.file_field.setStyleSheet(css(
            '''
            QLabel {
                padding: 20px;
                background: #444;
                border-radius: 8px;
            }
            '''
        ))
        clickable(self.file_field).connect(self.select_location)
        self.layout.addWidget(self.file_field)
        self.setLayout(self.layout)

    def select_location(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            new_path = dialog.selectedFiles()[0]
            UserSettingsSignal.put.emit('file_storage_location', new_path)
            self.file_field.setText(new_path)


class UserSettings(QWidget):

    def __init__(self):
        super(UserSettings, self).__init__()
        UserSettingsSignal.put.connect(self.update)
        self.settings = self.load()
        self.layout = QVBoxLayout(alignment=Qt.AlignTop)
        self.layout.setMargin(25)
        self.layout.addWidget(FileStorageLocation(self.settings))
        self.setLayout(self.layout)

    def load(self):
        return {
            'file_storage_location': '{}/Downloads'.format(os.path.expanduser('~')),
        }

    def update(self, key, value):
        self.settings[key] = value
