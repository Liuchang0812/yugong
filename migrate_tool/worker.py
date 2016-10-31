# -*- coding:utf-8 -*-
from Queue import Queue
from threading import Thread

class Worker(object):
    def __init__(self, threads_num=10):
        self._threads_num = threads_num
        self._threads_pool = []
        self._queue = Queue()

    def add_task(self, task):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    @property
    def success_num(self):
        pass

    def failure_num(self):
        pass