# -*- coding:utf-8 -*-
from Queue import Queue, Empty
from threading import Thread
from os import path, makedirs
from logging import getLogger

logger = getLogger(__name__)

class Worker(object):
    def __init__(self, work_dir, file_filter, input_service, output_service, threads_num=10, max_size=30):
        self._input_service = input_service
        self._output_service = output_service
        self._filter = file_filter
        self._work_dir = work_dir

        self._threads_num = threads_num
        self._threads_pool = []
        self._queue = Queue(maxsize=max_size)
        self._stop = False
        self._succ = 0
        self._fail = 0

    def __work_thread(self):

        while not self._stop:
            try:
                task = self._queue.get(timeout=1)
                self._queue.task_done()
            except Empty:
                continue
            
            localpath = path.join(self._work_dir, task)
            try:
                makedirs(path.dirname(localpath))
            except OSError as e:
                # directory is exists
                logger.debug(str(e))
            try:
                self._output_service.download(task, path.join(self._work_dir, task))
            except Exception as e:
                logger.exception(str(e))
                self._fail += 1
                continue

            try:
                self._input_service.upload(task, path.join(self._work_dir, task))
            except Exception as e:
                logger.exception(str(e))
                self._fail += 1
                continue

            # try:
            #     import shutil
            #     shutil.rmtree(path.join(self._work_dir, task))
            # except Exception as e:
            #     logger.exception(str(e))
            #     continue
            self._succ += 1

    def add_task(self, task):
        # blocking
        self._queue.put(task)

    def start(self):
        self._threads_pool = [Thread(target=self.__work_thread) for _ in range(self._threads_num)]
        for t in self._threads_pool:
            t.start()

    def stop(self):

        self._stop = True
        while any([t.is_alive() for t in self._threads_pool]):
            map(lambda i: i.join(5), filter(lambda j: j.is_alive(), self._threads_pool))

    @property
    def success_num(self):
        return self._succ

    @property
    def failure_num(self):
        return self._fail
