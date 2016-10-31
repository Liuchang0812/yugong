# -*- coding: utf-8 -*-

import os
from os import path

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

    def __init__(self, *args, **kwargs):

        self._workers = None
        self._input_service = None
        self._output_service = None
        self._filter = None

        self._work_dir = path.join(kwargs['work_dir'] or os.getcwd(), 'migrate_dir')
        self._worker = Worker(*args, **kwargs)
        self._input_service = None