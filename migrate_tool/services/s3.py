# -*- coding: utf-8 -*-

from logging import getLogger
from migrate_tool import storage_service
from migrate_tool.task import Task

from boto.s3.connection import S3Connection


logger = getLogger(__name__)


class S3StorageService(storage_service.StorageService):
    def __init__(self, *args, **kwargs):

        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        region = kwargs['region'] 
        self._prefix = kwargs['prefix'] if 'prefix' in kwargs else ''

        if region == 'cn-north-1':
            _s3_api = S3Connection(aws_access_key_id=accesskeyid, aws_secret_access_key=accesskeysecret, host='s3.cn-north-1.amazonaws.com.cn')
        else:
            _s3_api = S3Connection(aws_access_key_id=accesskeyid, aws_secret_access_key=accesskeysecret)

        _s3_api = S3Connection(aws_access_key_id=accesskeyid, aws_secret_access_key=accesskeysecret)
        self._bucket_api = _s3_api.get_bucket(bucket)

    def download(self, task, local_path):
        for i in range(20):
            key = self._bucket_api.get_key(task.key)

            if key is not None:
                key.get_contents_to_filename(local_path)
            else:
                raise IOError("Download failed 404")
            if task.size is None:
                logger.info("task's size is None, skip check file size on local")
                break

            from os import path
            if path.getsize(local_path) != int(task.size):
                logger.error("Download Failed, size1: {size1}, size2: {size2}".format(size1=path.getsize(local_path),
                                                                                      size2=task.size))
            else:
                logger.info("Download Successfully, break")
                break
        else:
            raise IOError("download failed with 20 retry")

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        for obj in self._bucket_api.list(prefix=self._prefix):
            if obj.name[-1] == '/':
                continue
            logger.info("yield new object: {}".format(obj.key))
            yield Task(obj.name, obj.size, None)

    def exists(self, _path):
        raise NotImplementedError
