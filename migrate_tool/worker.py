# -*- coding:utf-8 -*-
from Queue import Queue
from threading import Thread

class Worker(object):
    def __init__(self, filter, input_service, output_service, threads_num=10):
        self._input_service = input_service
        self._output_service = output_service
        self._filter = filter

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
        return 0

    @property
    def failure_num(self):
        return 0