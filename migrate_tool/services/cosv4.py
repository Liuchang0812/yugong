# -*- coding: utf-8 -*-


from migrate_tool import storage_service
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest, StatFileRequest

from logging import getLogger

logger = getLogger(__name__)


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
        self._overwrite = kwargs['overwrite'] == 'true' if 'overwrite' in kwargs else False

    def download(self, cos_path, local_path):
        raise NotImplementedError

    def upload(self, cos_path, local_path):
        if not cos_path.startswith('/'):
            cos_path = '/' + cos_path

        if self._prefix_dir:
            cos_path = self._prefix_dir + cos_path

        if isinstance(local_path, unicode):
            local_path.encode('utf-8')
        insert_only = 0 if self._overwrite else 1
        upload_request = UploadFileRequest(self._bucket, unicode(cos_path), local_path, insert_only=insert_only)
        upload_file_ret = self._cos_api.upload_file(upload_request)

        if upload_file_ret[u'code'] != 0:
            raise OSError("UploadError: " + str(upload_file_ret))

    def list(self):
        raise NotImplementedError

    def exists(self, _path):
        logger.info("exists: " + str(_path))
        request = StatFileRequest(self._bucket, _path)
        ret = self._cos_api.stat_file(request)
        logger.info("ret: " + str(ret))
        import json
        v = json.loads(ret)
        if v['code'] != 0:
            logger.warn("error code: " + v['error_code'])
            return False
        if v['data']['filelen'] != v['data']['filesize']:
            logger.warn("file is broken, filelen: {len}, filesize: {size}".format(
                len=v['data']['filelen'],
                size=v['data']['filesize']
            ))
            return False
        return True
