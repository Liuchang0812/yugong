# -*- coding: utf-8 -*-


from logging import getLogger
from migrate_tool import storage_service
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest, StatFileRequest


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

    def upload(self, task, local_path):
        cos_path = task.key
        if not cos_path.startswith('/'):
            cos_path = '/' + cos_path

        if self._prefix_dir:
            cos_path = self._prefix_dir + cos_path

        if isinstance(local_path, unicode):
            local_path.encode('utf-8')
        insert_only = 0 if self._overwrite else 1
        for i in range(10):
            try:
                upload_request = UploadFileRequest(self._bucket, unicode(cos_path), local_path, insert_only=insert_only)
                upload_file_ret = self._cos_api.upload_file(upload_request)

                if upload_file_ret[u'code'] != 0:
                    raise OSError("UploadError: " + str(upload_file_ret))
                else:
                    break
            except:
                pass
        else:
            raise IOError("upload failed")

    def list(self):
        raise NotImplementedError

    def exists(self, task):
        _path = task.key
        _size = task.size

        if not _path.startswith('/'):
            _path = '/' + _path
        logger = getLogger(__name__)
        logger.info("func: exists: " + str(_path))
        if self._prefix_dir:
            _path = self._prefix_dir + _path

        if isinstance(_path, str):
            _path = _path.decode('utf-8')
        request = StatFileRequest(self._bucket, _path)
        ret = self._cos_api.stat_file(request)
        logger.info("ret: " + str(ret))
        # import json
        # v = json.loads(ret)
        if ret['code'] != 0:
            logger.warn("error code: " + str(ret['code']))
            return False
        if ret['data']['filelen'] != ret['data']['filesize']:
            logger.warn("file is broken, filelen: {len}, filesize: {size}".format(
                len=ret['data']['filelen'],
                size=ret['data']['filesize']
            ))
            return False
        elif _size is not None and ret['data']['filelen'] != _size:
            return False
        elif ret['data']['filelen'] != _size:
            return False
        return True
