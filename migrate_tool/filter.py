# -*- coding: utf-8 -*-

import leveldb
from os import path
from time import time


class Filter(object):

    def __init__(self, work_dir, record_succ=True):
        self._workdir = work_dir
        self._db = leveldb.LevelDB(path.join(self._workdir, 'leveldb'))
        self._marker_db = leveldb.LevelDB(path.join(self._workdir, 'markerdb'))
        self._doing_task_db = leveldb.LevelDB(path.join(self._workdir, 'doingtaskdb'))
        self._record_succ = record_succ

    def add(self, value):
        if not self._record_succ:
            return
            
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._db.Put(value, str(time()))

    def query(self, value):
        if not self._record_succ:
            return False

        try:
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            self._db.Get(value)
            return True
        except KeyError:
            return False

    def add_doing_task(self, value):
        if self._record_succ:
            return

        if isinstance(value, unicode):
	    value = value.encode('utf-8')
	self._doing_task_db.Put(value, str(time()))
   
    def del_doing_task(self, value):
        if self._record_succ:
            return
        try:
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            self._doing_task_db.Delete(value)
            return True
        except KeyError:
            return False

    def list_doing_task(self):
        keys = list(self._doing_task_db.RangeIter(include_value = False))
        return keys

    def set_marker(self, value):
        if self._record_succ:
            return

        if isinstance(value, unicode):
	    value = value.encode('utf-8')
	self._db.Put("listmarker", value)

    def get_marker(self):
        if self._record_succ:
            return ''

        try:
            value = self._db.Get("listmarker")
            return value 
        except KeyError:
            return ""

    def reset(self):
        self.clear_db(self._db)
        self.clear_db(self._marker_db)
        self.clear_db(self._doing_task_db)
 
    def clear_db(self, db):
	b = leveldb.WriteBatch()  
	for k in db.RangeIter(include_value = False, reverse = True):  
            b.Delete(k)  
	db.Write(b)  
