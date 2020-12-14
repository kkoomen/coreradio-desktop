#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QFileDialog, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from utils import css
from widgets.buttons import IconButton
from signals import UserSettingsSignal
from constants import SETTINGS_FILE
import json
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

        file_field_container = QWidget()
        file_field_container_layout = QHBoxLayout()
        file_field_container_layout.setMargin(0)
        file_field_container.setLayout(file_field_container_layout)

        self.file_label = QLabel(self.settings['file_storage_location'])
        self.file_label.setStyleSheet(css(
            '''
            QLabel {
                padding: 20px;
                background: #444;
                border-radius: 8px;
            }
            '''
        ))
        file_field_container_layout.addWidget(self.file_label)

        change_btn = IconButton(text='Change', on_click=self.select_location)
        change_btn.setFixedWidth(100)
        file_field_container_layout.addWidget(change_btn)

        self.layout.addWidget(file_field_container)
        self.setLayout(self.layout)

    def select_location(self):
        dialog = QFileDialog(self, 'File Storage Location', self.settings['file_storage_location'])
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            new_path = dialog.selectedFiles()[0]
            UserSettingsSignal.put.emit('file_storage_location', new_path)
            self.file_label.setText(new_path)


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
        if not os.path.exists(SETTINGS_FILE):
            default_settings = {
                'file_storage_location': '{}/Downloads'.format(os.path.expanduser('~')),
            }
            self.save(default_settings)
            return default_settings

        return json.loads(open(SETTINGS_FILE, 'r').read())

    def update(self, key, value):
        self.settings[key] = value
        self.save()

    def save(self, settings=None):
        contents = self.settings if settings is None else settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(contents, f)
            f.close()
