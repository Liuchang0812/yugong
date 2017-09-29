# -*- coding: utf-8 -*

from logging import getLogger
from migrate_tool import storage_service
from qcloud_cos_v5 import CosS3Client, CosConfig

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

        conf = CosConfig(Appid=appid, Access_id=str(accesskeyid), Access_key=str(accesskeysecret),
                         Region=region)
        self._cos_client = CosS3Client(conf=conf, retry=1)
        self._bucket = bucket
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

        for j in range(5):
            try:
                fp = open(local_path, "rb")
                self._cos_client.put_object(Bucket=self._bucket, Body=fp, Key=cos_path)
                fp.close()
                break
            except Exception as e:           
                logger.warn('upload failed %s' % str(e))
                fp.close()
        else:
            raise OSError("uploaderror")

    def list(self):
        raise NotImplementedError

    def exists(self, task):
        cos_path = task.key
        #cos_path = 'http://' + str(self._bucket) + '-' + str(self._appid) + '.' + str(self._region) + '.myqcloud.com' + '/' + str(cos_path)
        logger.debug('{}'.format(str({'cos_path:': cos_path})))
        try:
            self._cos_client.head_object(Key=cos_path, Bucket=self._bucket)
        except:
            logger.exception("head cos file failed")
            return False
        return True
