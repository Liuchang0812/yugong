# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from os import path
from logging import getLogger
from threading import Timer, Thread

from migrate_tool.worker import Worker
from migrate_tool.filter import Filter
logger = getLogger('__name__')


class BaseMigrator(object):

    def start(self):
        pass

    def stop(self):
        pass

    @property
    def status(self):
        """ Query migrate status

        :return: dict like {'success': 213, 'failure': 19}
        """
        pass


class ThreadMigrator(BaseMigrator):
    """migrator Class, consisted of:
        1. Workers
        2. InputStorageService
        3. OutputStorageService
        4. Filter: Determines whether the file has been moved

    """

    def __init__(self, input_service, output_service, work_dir=None, threads=10, *args, **kwargs):

        self._input_service = input_service
        self._output_service = output_service

        self._work_dir = work_dir or os.getcwd()
        self._filter = Filter()


        self._worker = Worker(filter=self._filter, input_service=self._input_service, output_service=self._output_service, threads_num=threads)

        self._stop = False
        self._finish = False
        self._threads = []
        #if path.exists(path.join(self._work_dir, 'filter.json')):
        #    with open(path.join(self._work_dir, 'filter.json'), 'r') as f:
        #       self._filter.loads(f.read())
        #        logger.info("loads bloom filter snapshot successfully.")

    def log_status_thread(self):
        while not self._stop and not self._finish:
            logger.info("yugong is working, {} tasks successfully, {} tasks failed.".format(self._worker.success_num, self._worker.failure_num()))

    def work_thread(self):
        assert self._output_service is None

        for object_name in self._output_service.list():

            if self._stop:
                break

            if self._filter.query(object_name):
                # object had been migrated
                logger.info("{} has been migrated, skip it".format(object_name))

            else:
                # not migrated
                self._worker.add_task(object_name)
                logger.info("{} has been submitted, waiting for migrating".format(object_name))
        else:
            self._finish = True

    def start(self):
        log_status_thread = Thread(target=self.log_status_thread, name='log_status_thread')
        log_status_thread.daemon = True
        self._threads.append(log_status_thread)

        work_thread = Thread(target=self.work_thread, name='work_thread')
        work_thread.daemon = True
        self._threads.append(work_thread)

        for t in self._threads:
            t.start()

    def stop(self):
        self._stop = True

        for t in self._threads:
            t.join()
