# -*- coding: utf-8 -*-

from logging import getLogger
from migrate_tool import storage_service
import oss2
logger = getLogger(__name__)


class OssStorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        endpoint = kwargs['endpoint']
        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        self._oss_api = oss2.Bucket(oss2.Auth(accesskeyid, accesskeysecret), endpoint, bucket)

    def download(self, cos_path, local_path):
        self._oss_api.get_object_to_file(cos_path, local_path)

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        for obj in oss2.ObjectIterator(self._oss_api):
            if obj.key[-1] == '/':
                continue
            logger.info("yield new object: {}".format(obj.key))
            yield obj.key

    def exists(self, _path):
        raise NotImplementedError
