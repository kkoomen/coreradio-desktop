#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et


"""
Runs a function in a thread, and alerts the parent when done.

Uses a Signal to alert the main thread of completion.
"""


from PySide2.QtCore import QThread, Signal
import logging


class RunThread(QThread):
    finished = Signal(["QString"], [int])

    def __init__(self, func, on_finish, *args, **kwargs):
        super(RunThread, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.func = func
        if on_finish is not None:
            self.finished.connect(on_finish)
            self.finished[int].connect(on_finish)
        else:
            self.finished = None
        self.start()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as err:
            logging.info('Could not run thread function: {}'.format(err))
            result = err
        finally:
            if self.finished is not None:
                if isinstance(result, int):
                    self.finished[int].emit(result)
                else:
                    self.finished.emit(str(result))
