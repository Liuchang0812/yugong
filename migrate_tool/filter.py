# -*- coding: utf-8 -*-

class Filter(object):
    """TODO: use sqlite to filte files which have been migrated"""

    def __init__(self, work_dir):
        self._workdir = work_dir

    def add(self, value):
        pass

    def query(self, value):
        return False
