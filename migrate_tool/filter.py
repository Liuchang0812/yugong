# -*- coding: utf-8 -*-

class Filter(object):
    """TODO: use sqlite to filter files which are migrated"""

    def __init__(self, work_dir):
        self._workdir = work_dir

    def add(self, value):
        pass

    def query(self, value):
        return False