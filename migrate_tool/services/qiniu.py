# -*- coding: utf-8 -*-
from __future__ import absolute_import

from logging import getLogger
from migrate_tool import storage_service
from qiniu import Auth
from qiniu import BucketManager
import requests

logger = getLogger(__name__)


class QiniuStorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        self._bucket = kwargs['bucket']
        self._auth = Auth(accesskeyid, accesskeysecret)
        self._domain = kwargs['domain_url']
        self._qiniu_api = BucketManager(self._auth)

    def download(self, cos_path, local_path):
        if isinstance(local_path, str):
            local_path = local_path.decode('utf-8')
        if cos_path.startswith('/'):
            cos_path = cos_path[1:]

        if isinstance(cos_path, unicode):
            cos_path = cos_path.encode('utf-8')
            from urllib import quote
            cos_path = quote(cos_path)

        base_url = 'http://%s/%s' % (self._domain, cos_path)
        print base_url
        private_url = self._auth.private_download_url(base_url, expires=3600)
        print private_url
        logger.debug("private url: " + private_url)

        ret = requests.get(private_url)

        if ret.status_code != 200:
            raise SystemError("download file from qiniu failed")
        print local_path.encode('utf-8')
        with open(local_path.encode('utf-8'), 'wb') as fd:
            for chunk in ret.iter_content(1024):
                fd.write(chunk)

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        prefix = None
        limit = 100
        delimiter = None
        marker = None

        eof = False

        while not eof:
            try:
                ret, eof, info = self._qiniu_api.list(self._bucket, prefix, marker, limit, delimiter)
                for i in ret['items']:
                    yield i['key']

                if not eof and 'marker' in ret:
                    marker = ret['marker']
                else:
                    eof = True
            except Exception as e:
                logger.exception("list exception: " + str(e))

    def exists(self, _path):
        raise NotImplementedError
