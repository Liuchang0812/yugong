# -*- coding: utf-8 -*-


from migrate_tool import storage_service
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest


class CosV4StorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        appid = int(kwargs['appid'])
        region = kwargs['region']
        accesskeyid = unicode(kwargs['accesskeyid'])
        accesskeysecret = unicode(kwargs['accesskeysecret'])
        bucket = unicode(kwargs['bucket'])
        if 'prefix_dir' in kwargs:
            self._prefix_dir = kwargs['prefix_dir']
        else:
            self._prefix_dir = None

        self._cos_api = CosClient(appid, accesskeyid, accesskeysecret, region=region)
        self._bucket = bucket


    def download(self, cos_path, local_path):
        raise NotImplementedError

    def upload(self, cos_path, local_path):
        if not cos_path.startswith('/'):
            cos_path = '/' + cos_path

        if self._prefix_dir:
            cos_path = self._prefix_dir + cos_path


        if isinstance(local_path, unicode):
            local_path.encode('utf-8')

        upload_request = UploadFileRequest(self._bucket, unicode(cos_path), local_path)
        upload_file_ret = self._cos_api.upload_file(upload_request)

        if upload_file_ret[u'code'] != 0:
            raise OSError("UploadError: " + str(upload_file_ret))

    def list(self):
        raise NotImplementedError

    def exists(self, _path):
        raise NotImplementedError
