# -*- coding: utf-8 -*-


from migrate_tool import storage_service
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest

class CosV4StorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        appid = kwargs['appid']
        region = kwargs['region']
        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        self._cos_api = CosClient(appid, accesskeyid, accesskeysecret, region=region)
        self._bucket = bucket


    def download(self, cos_path, local_path):
        raise NotImplementedError

    def upload(self, cos_path, local_path):
        upload_request = UploadFileRequest(self._bucket, unicode(cos_path), unicode(local_path))
        upload_file_ret = self._cos_api.upload_file(upload_request)

        if upload_file_ret[u'code'] != 0:
            raise OSError("UploadError: " + str(upload_file_ret))

    def list(self):
        raise NotImplementedError

    def exists(self, _path):
        raise NotImplementedError
