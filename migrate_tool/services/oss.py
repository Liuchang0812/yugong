# -*- coding: utf-8 -*-


from migrate_tool import storage_service
import oss2

class OssStorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        print args
        print kwargs
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
            yield obj.key

    def exists(self, _path):
        raise NotImplementedError
