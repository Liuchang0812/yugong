# -*- coding: utf-8 -*-

from logging import getLogger
from migrate_tool import storage_service
from boto.s3.connection import S3Connection

logger = getLogger(__name__)


class S3StorageService(storage_service.StorageService):
    def __init__(self, *args, **kwargs):

        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        _s3_api = S3Connection(aws_access_key_id=accesskeyid, aws_secret_access_key=accesskeysecret)
        self._bucket_api = _s3_api.get_bucket(bucket)

    def download(self, cos_path, local_path):
        key = self._bucket_api.get_key(cos_path)
        if key is not None:
            key.get_contents_to_filename(local_path)

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        for obj in self._bucket_api.list():
            if obj.name[-1] == '/':
                continue
            logger.info("yield new object: {}".format(obj.key))
            yield obj.name

    def exists(self, _path):
        raise NotImplementedError
