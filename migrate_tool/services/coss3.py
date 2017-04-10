# -*- coding: utf-8 -*

from logging import getLogger
from migrate_tool import storage_service
from coscmd.client import CosS3Client, CosConfig, CosS3Auth

from migrate_tool.task import Task
import requests


def to_unicode(s):
    if isinstance(s, str):
        return s.decode('utf-8')
    else:
        return s


def to_utf8(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return s


logger = getLogger(__name__)


class CosS3StorageService(storage_service.StorageService):

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

        if 'part_size' in kwargs:
            self._part_size = kwargs['part_size']
        else:
            self._part_size = 1

        conf = CosConfig(appid=appid, access_id=str(accesskeyid), access_key=str(accesskeysecret),
                         region=region, bucket=bucket, part_size=self._part_size)
        self._cos_client = CosS3Client(conf)
        self._bucket = bucket
        self._overwrite = kwargs['overwrite'] == 'true' if 'overwrite' in kwargs else False
        self._max_retry = 20
        self._appid = appid
        self._region = region
        self._accesskeyid = str(accesskeyid)
        self._accesskeysecret = str(accesskeysecret)

    def download(self, task, local_path):
        # self._oss_api.get_object_to_file(urllib.unquote(cos_path).encode('utf-8'), local_path)
        raise NotImplementedError

    def upload(self, task, local_path):
        cos_path = task.key
        if not cos_path.startswith('/'):
            cos_path = '/' + cos_path

        if self._prefix_dir:
            cos_path = self._prefix_dir + cos_path

        if isinstance(local_path, unicode):
            local_path.encode('utf-8')
        if cos_path.startswith('/'):
            cos_path = cos_path[1:]

        insert_only = 0 if self._overwrite else 1
        mp = self._cos_client.multipart_upload_from_filename(local_path, cos_path)
        for i in range(10):
            rt = mp.init_mp()
            if rt:
                break
            logger.warn("init multipart upload failed")
        else:
            raise IOError("upload failed")

        for i in range(10):
            rt = mp.upload_parts()
            if rt:
                break
            logger.warn("multipart upload part failed")
        else:
            raise IOError("upload failed")

        for i in range(10):
            rt = mp.complete_mp()
            if rt:
                break
            logger.warn("finish upload part failed")
        else:
            raise IOError("upload failed")

    def list(self):
        raise NotImplementedError

    def exists(self, task):
        cos_path = task.key
        cos_path = 'http://' + str(self._bucket) + '-' + str(self._appid) + '.' + str(self._region) + '.myqcloud.com' + '/' + str(cos_path)
        logger.debug('{}'.format(str({'cos_path:': cos_path})))
        try:
            ret = requests.head(cos_path, timeout=10, auth=CosS3Auth(self._accesskeyid, self._accesskeysecret))
            if ret.status_code != 200:
                return False
            else:
                return True
        except:
            logger.exception("head cos file failed")
            return False
        return True
