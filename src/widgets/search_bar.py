#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
TODO
"""


from PySide2.QtCore import Qt, QStringListModel
from PySide2.QtWidgets import QLineEdit, QVBoxLayout, QCompleter, QVBoxLayout, QWidget
from utils import css
from widgets.run_thread import RunThread
from widgets.song_detail_page import SongDetailPage
from spider import CoreRadioSpider
from signals import PageSignal
import colors
import logging


class SearchBar(QWidget):

    def __init__(self):
        super(SearchBar, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)
        self.setStyleSheet(css('border: 1px solid {{color}};', color=colors.SECONDARY_COLOR))

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText('Try searching for an artist or album')
        self.searchbar.textChanged.connect(self.set_keywords)
        self.searchbar.returnPressed.connect(self.search)
        self.searchbar.setStyleSheet(css(
            '''
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                background: {{backgroundColor}};
            }
            ''',
            backgroundColor=colors.PLACEHOLDER_COLOR
        ))

        self.layout.addWidget(self.searchbar)
        self.setLayout(self.layout)

    def set_keywords(self, keywords):
        self.keywords = keywords

    def search(self):
        if self.searchbar.completer() and self.searchbar.completer().popup().isVisible():
            # User did select an option from the dropdown menu.
            selected_suggestion = [s for s in self.suggestions if s['label'] == self.keywords]
            if len(selected_suggestion) > 0:
                self.searchbar.setCompleter(None)
                PageSignal.changed.emit(SongDetailPage(url=selected_suggestion[0]['url']))
        else:
            # User did type something and then hit ENTER to search.
            self.thread = RunThread(self.get_search_suggestions, self.on_search_suggestions)

    def get_search_suggestions(self):
        if self.keywords:
            self.searchbar.setEnabled(False)
            logging.info('Getting search suggestions for keywords: "{}"'.format(self.keywords))
            spider = CoreRadioSpider()
            self.suggestions = spider.get_search_suggestions(self.keywords)

    def on_search_suggestions(self):
        logging.info('Received search suggestions for keywords: "{}"'.format(self.keywords))
        self.searchbar.setEnabled(True)
        self.searchbar.setFocus()
        if self.suggestions:
            suggestions = [suggestion['label'] for suggestion in self.suggestions]
            completer = QCompleter(suggestions)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.searchbar.setCompleter(completer)
            self.searchbar.completer().complete()
            self.searchbar.completer().popup().setStyleSheet(css(
                """
                QListView {
                    border: 1px solid {{borderColor}};
                    padding: 10px;
                    background: {{backgroundColor}};
                }
                QItemSelection {
                    padding: 10px;
                }
                """,
                borderColor=colors.SECONDARY_COLOR,
                backgroundColor=colors.PLACEHOLDER_COLOR,
            ))
