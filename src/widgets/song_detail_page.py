#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QScrollArea, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy, QPushButton, QGridLayout, QDialog
from PySide2.QtGui import QImage, QPixmap, QIcon, QFont
from widgets.run_thread import RunThread
from widgets.buttons import IconButton
from spider import CoreRadioSpider
from typography import H1
from utils import css, clickable, replace_multiple
import colors
import time
import requests
import sys


class Song(QWidget):

    def __init__(self, song=None, index=None):
        super(Song, self).__init__()
        self.song = song

        color = '#fff' if self.song['released'] else '#666'
        self.setStyleSheet(css('color: {{color}};', color=color))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        label = '{}.  {}'.format(index, self.song['name'])
        self.layout.addWidget(QLabel(label))
        self.setLayout(self.layout)


class Songlist(QWidget):

    def __init__(self, songlist=None):
        super(Songlist, self).__init__()
        self.songlist = songlist

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(25)
        for index, song in enumerate(self.songlist):
            self.layout.addWidget(Song(song=song, index=index+1))
        self.setLayout(self.layout)


class Header(QWidget):

    def __init__(self, song=None):
        super(Header, self).__init__()
        self.song = song
        self.layout = QGridLayout()
        self.layout.setMargin(0)
        self.layout.setContentsMargins(0, 0, 0, 25)

        self.setObjectName(u'header')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(css(
            '''
            #header {
                border-bottom: 1px solid {{backgroundColor}};
            }
            ''',
            backgroundColor=colors.SECONDARY_COLOR
        ))

        self.left_container = QWidget()
        self.left_container.setStyleSheet(css('color: {{color}};', color=colors.GREY_COLOR))
        self.left_container_layout = QHBoxLayout(alignment=Qt.AlignLeft)
        self.left_container_layout.setMargin(0)
        self.left_container.setLayout(self.left_container_layout)

        self.right_container = QWidget()
        self.right_container_layout = QHBoxLayout(alignment=Qt.AlignRight)
        self.right_container_layout.setMargin(0)
        self.right_container.setLayout(self.right_container_layout)

        self.layout.addWidget(self.left_container, 0, 0)
        self.layout.addWidget(self.right_container, 0, 1)

        # Info on the left
        info_text = '{} · {} songs'.format(self.song['genre'], len(self.song['songlist'])).upper()
        self.left_container_layout.addWidget(QLabel(info_text))

        # Download buttons on the right
        if 'download_links' in self.song:
            for item in self.song['download_links']:
                btn = IconButton(text=item['label'],
                                 icon='download',
                                 on_click=self.download(item))
                self.right_container_layout.addWidget(btn)

        self.setLayout(self.layout)

    def download_song(self, item, filename):
        res = requests.get(item['url'], stream=True)
        print('GET {}'.format(item['url']))

        total_length = int(res.headers.get('content-length'))
        current_length = 1
        with open('/Users/jinkeming/NewMusic/{}'.format(filename), 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    current_length += len(chunk)
                    download_percentage = int(100 / total_length * current_length)
                    download_text = '\n'.join([
                        'Downloaded: {}%'.format(download_percentage),
                        'Title: {}'.format(self.song['title']),
                        'Quality: {}'.format(item['label']),
                        'Saving as: {}'.format(filename),
                    ])
                    self.download_text_label.setText(download_text)
                    sys.stdout.write('\r{}% Downloading {} (Saving as: {})'.format(download_percentage, self.song['title'], filename))
                    file.write(chunk)
            sys.stdout.write('\n')
            file.close()
        return True


    def on_download_song_complete(self):
        self.download_dialog.setWindowFlags(
            Qt.WindowCloseButtonHint |
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowMinimizeButtonHint
        )
        self.download_dialog.show()

    def download(self, item):
        def closure():
            self.download_dialog = QDialog()
            self.download_dialog.setWindowFlags(
                Qt.Window |
                Qt.CustomizeWindowHint |
                Qt.WindowTitleHint |
                Qt.WindowMinimizeButtonHint
            )
            self.download_dialog.setModal(True)
            self.download_dialog_layout = QVBoxLayout()
            self.download_text_label = QLabel()
            font = QFont()
            font.setKerning(False)
            self.download_text_label.setFont(font)
            self.download_dialog_layout.addWidget(self.download_text_label)
            self.download_dialog.setLayout(self.download_dialog_layout)

            filename = replace_multiple(self.song['title'], (
                (r'\s+', '_'),
                (r'[^\w]+', ''),
                (r'_+', '_'),
            )).lower()
            filename = '{}.tar'.format(filename)

            download_text = '\n'.join([
                'Downloaded: 0%',
                'Title: {}'.format(self.song['title']),
                'Quality: {}'.format(item['label']),
                'Saving as: {}'.format(filename),
            ])
            self.download_text_label.setText(download_text)

            self.download_thread = RunThread(self.download_song, self.on_download_song_complete, item, filename)
            self.download_dialog.exec()
        return closure


class SongDetailPage(QWidget):

    def __init__(self, url=None):
        super(SongDetailPage, self).__init__()
        self.url = url
        self.loading = False
        self.image_content = None
        self.image_size = 400
        self.song = None

        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        self.page_widget = QScrollArea()
        self.page_widget.setWidgetResizable(True)

        widget = QWidget(self.page_widget)
        widget.setMinimumWidth(800)
        self.page_widget.setWidget(widget)

        self.page_layout = QVBoxLayout(widget, alignment=Qt.AlignTop)
        self.page_layout.setContentsMargins(25, 25, 25, 25)

        self.layout.addWidget(self.page_widget)
        self.setLayout(self.layout)

        self.thread = RunThread(self.get_song_info, self.on_song_info)

    def render_song_info(self):
        # Header
        self.page_layout.addWidget(Header(song=self.song))

        # Title
        title = H1(self.song['title'])
        title.setWordWrap(True)
        self.page_layout.addWidget(title)

        # Inner container that contains Image + Songlist
        inner_container = QWidget()
        inner_container_layout = QHBoxLayout(alignment=Qt.AlignTop|Qt.AlignLeft)
        inner_container_layout.setMargin(0)
        inner_container_layout.setSpacing(25)
        inner_container_layout.setContentsMargins(0, 25, 0, 0)
        inner_container.setLayout(inner_container_layout)
        self.page_layout.addWidget(inner_container)

        # Image
        self.image_label = QLabel()
        self.image_label.setStyleSheet('background-color: #252525;')
        self.image_label.setMinimumWidth(self.image_size)
        self.image_label.setMinimumHeight(self.image_size)
        inner_container_layout.addWidget(self.image_label, alignment=Qt.AlignTop)
        self.get_image_thread = RunThread(self.fetch_image, self.on_image_loaded)

        # Songlist
        inner_container_layout.addWidget(
            Songlist(songlist=self.song['songlist']),
            alignment=Qt.AlignTop)

    def fetch_image(self):
        time.sleep(1)
        print('GET {}'.format(self.song['image']))
        try:
            response = requests.get(self.song['image'])
            self.image_content = response.content
        except Exception as e:
            return True
        return True

    def on_image_loaded(self):
        if self.image_content:
            imgWidget = QImage()
            imgWidget.loadFromData(self.image_content)
            picture = QPixmap(imgWidget)
            picture = picture.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)
            self.image_label.setPixmap(picture)
            print('[DONE] GET {}'.format(self.song['image']))
        else:
            print('[FAILED] GET {}'.format(self.song['image']))

    def get_song_info(self):
        self.loading = True
        spider = CoreRadioSpider()
        self.song = spider.get_song_info(url=self.url)
        return True

    def on_song_info(self):
        if self.song is not None:
            self.render_song_info()
            self.loading = False
        else:
            self.page_layout.addWidget(QLabel("Something wen't wrong"))
