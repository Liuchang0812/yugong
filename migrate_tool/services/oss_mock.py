# -*- coding: utf-8 -*-

from logging import getLogger
import urllib
from migrate_tool import storage_service
import oss2
logger = getLogger(__name__)


class OssMockStorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        endpoint = kwargs['endpoint']
        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        self._oss_api = oss2.Bucket(oss2.Auth(accesskeyid, accesskeysecret), endpoint, bucket)
        self._prefix = kwargs['prefix'] if 'prefix' in kwargs else ''
        if self._prefix.startswith('/'):
            self._prefix = self._prefix[1:]
        self._mis_file = kwargs['mis_file']

    def download(self, task, local_path):
	
        # self._oss_api.get_object_to_file(urllib.unquote(cos_path).encode('utf-8'), local_path)
        for i in range(20):
            logger.info("download file with rety {0}".format(i))
            import os
            try:
                os.remove(task['store_path'])
            except:
                pass

            self._oss_api.get_object_to_file(task['store_path'], local_path)
            from os import path
            if path.getsize(local_path) != int(task['size']):
                logger.error("Download Failed, size1: {size1}, size2: {size2}".format(size1=path.getsize(local_path), size2=task['size']))
            else:
                logger.info("Download Successcess, break")
                break
        else:
            raise IOError("Download Failed with 20 retry")

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        '''
        marker = ''
        while True:
            try:
                for obj in oss2.ObjectIterator(self._oss_api, prefix=self._prefix, marker=marker, max_keys=1000):
                    if obj.key[-1] == '/':
                        continue
                    # logger.info("yield new object: {}".format(urllib.quote(obj.key)))
                    # yield urllib.quote(obj.key)
                    # yield obj.key
                    yield {'store_path': obj.key, 'size': obj.size}
                    marker = obj.key
                break
            except Exception:
                logger.exception("list error")
          '''
        with open(self._mis_file, "r") as f:
            for line in f:
                try:
                    ret = line.split()
                    filename = ret[0]
                    size1 = ret[1]
                    int(size1)
                except:
                    continue
                yield {'store_path': filename[1:], 'size': size1}

    def exists(self, _path):
        raise NotImplementedError
