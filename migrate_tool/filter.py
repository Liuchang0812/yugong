# -*- coding: utf-8 -*-

import leveldb
from os import path
from time import time


class Filter(object):

    def __init__(self, work_dir):
        self._workdir = work_dir
        self._db = leveldb.LevelDB(path.join(self._workdir, 'leveldb'))

    def add(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._db.Put(value, str(time()))

    def query(self, value):
        try:
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            self._db.Get(value)
            return True
        except KeyError:
            return False
